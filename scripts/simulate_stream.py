import psycopg2
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.sprt_core import SPRT

# Подключение к БД
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="sprt_fraud",
    user="postgres",
    password="tromb404"
)

cursor = conn.cursor()

# Создаём таблицу алертов (если её нет)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts_python (
        alert_id SERIAL PRIMARY KEY,
        client_id INTEGER,
        txn_id INTEGER,
        alert_time TIMESTAMP,
        log_lr DOUBLE PRECISION
    )
""")
conn.commit()

# Загружаем параметры распределений из JSON (или используем стандартные)
try:
    import json
    with open('data/distribution_params.json', 'r') as f:
        params = json.load(f)
    h0_mu = params['H0']['mu']
    h0_sigma = params['H0']['sigma']
    h1_mu = params['H1']['mu']
    h1_sigma = params['H1']['sigma']
    print(f"Loaded params: H0(μ={h0_mu}, σ={h0_sigma}), H1(μ={h1_mu}, σ={h1_sigma})")
except:
    h0_mu, h0_sigma, h1_mu, h1_sigma = 3.0, 1.0, 5.0, 1.5
    print("Using default params")

# Инициализируем SPRT
sprt = SPRT(alpha=0.01, beta=0.001, 
            h0_mu=h0_mu, h0_sigma=h0_sigma,
            h1_mu=h1_mu, h1_sigma=h1_sigma)

print(f"SPRT thresholds: A={sprt.A:.2f}, B={sprt.B:.2f}")
print("-" * 50)

# Читаем транзакции
df = pd.read_csv("data/transactions_synthetic.csv")
df['txn_time'] = pd.to_datetime(df['txn_time'])

total_alerts = 0

for _, row in df.iterrows():
    client_id = int(row['client_id'])
    amount = row['amount']
    txn_time = row['txn_time']
    is_fraud_true = int(row['is_fraud'])
    
    # Вставляем транзакцию в БД
    cursor.execute("""
        INSERT INTO transactions (client_id, amount, txn_time, is_fraud)
        VALUES (%s, %s, %s, %s)
        RETURNING txn_id
    """, (client_id, amount, txn_time, is_fraud_true))
    
    txn_id = cursor.fetchone()[0]
    conn.commit()
    
    # Обновляем SPRT
    result = sprt.update(client_id, amount, txn_id)
    
    # Если алерт — сохраняем в БД
    if result == 'FRAUD':
        total_alerts += 1
        cursor.execute("""
            INSERT INTO alerts_python (client_id, txn_id, alert_time, log_lr)
            VALUES (%s, %s, NOW(), %s)
        """, (client_id, txn_id, sprt.log_lr[client_id]))
        conn.commit()
        print(f"🚨 ALERT! Client {client_id} | Txn {txn_id} | Amount: {amount:.2f} | LogLR: {sprt.log_lr[client_id]:.2f} | Fraud: {is_fraud_true}")
    else:
        status = "📊"
        if result == 'HONEST':
            status = "✅"
        print(f"{status} Client {client_id} | Txn {txn_id} | Amount: {amount:.2f} | LogLR: {sprt.get_state(client_id):.2f} | Fraud: {is_fraud_true}")
    
    time.sleep(0.001)  # небольшая задержка

print("-" * 50)
print(f"✅ Simulation complete. Total alerts: {total_alerts}")

cursor.close()
conn.close()