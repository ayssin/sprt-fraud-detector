"""
Симулятор потока транзакций для SPRT-детектора
Построчно читает CSV и "подаёт" транзакции в PostgreSQL
(пока просто выводит в консоль, без реального подключения к БД)
"""

import pandas as pd
import time
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *

def simulate_stream(csv_path, delay_seconds=0.01, max_txns=None):
    """
    Симулятор потока транзакций
    
    Parameters:
    - csv_path: путь к CSV с транзакциями
    - delay_seconds: задержка между транзакциями (сек)
    - max_txns: максимальное количество транзакций (для теста)
    """
    print(f"🚀 Запуск симулятора потока")
    print(f"   Файл: {csv_path}")
    print(f"   Задержка: {delay_seconds} сек")
    print(f"   Параметры SPRT: α={ALPHA}, β={BETA}")
    print("-" * 50)
    
    # Читаем CSV по частям (chunks) чтобы не загружать всё в память
    chunk_size = 1000
    total_processed = 0
    
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        for _, row in chunk.iterrows():
            # Здесь будет вызов SQL-функции update_sprt
            # Пока просто выводим информацию
            print(f"[{row['txn_id']}] Клиент {int(row['client_id'])} | "
                  f"Сумма: {row['amount']:.2f} | "
                  f"Фрод: {'✅' if row['is_fraud'] else '❌'} | "
                  f"Время: {row['txn_time'][:19]}")
            
            total_processed += 1
            
            if max_txns and total_processed >= max_txns:
                print(f"\n⏹️  Достигнут лимит {max_txns} транзакций")
                return
            
            # Задержка для имитации реального потока
            time.sleep(delay_seconds)
    
    print(f"\n✅ Симуляция завершена. Обработано {total_processed} транзакций")

if __name__ == "__main__":
    # Тестовый запуск на 20 транзакциях
    simulate_stream(
        csv_path="data/transactions_synthetic.csv",
        delay_seconds=0.05,
        max_txns=20
    )