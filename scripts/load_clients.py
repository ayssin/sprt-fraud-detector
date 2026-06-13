import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="sprt_fraud",
    user="postgres",
    password="tromb404"
)

cursor = conn.cursor()

clients_df = pd.read_csv("data/clients.csv")

for _, row in clients_df.iterrows():
    cursor.execute("""
        INSERT INTO clients (client_id, client_name)
        VALUES (%s, %s)
        ON CONFLICT (client_id) DO NOTHING
    """, (int(row['client_id']), row['client_name']))
    conn.commit()
    print(f"Added client {int(row['client_id'])}")

cursor.close()
conn.close()
print("All clients loaded!")
