# SPRT Fraud Detector

Online-детектор мошеннических транзакций на основе последовательного анализа Вальда


## О проекте

SPRT Fraud Detector — реализация последовательного анализа Вальда для обнаружения мошеннических транзакций в реальном времени.

В отличие от классических ML-моделей, которые работают батчами, SPRT анализирует каждую транзакцию моментально и принимает решение, накопил ли алгоритм достаточно статистических доказательств.

Ключевые особенности:
- Онлайн-режим — решение после каждой транзакции
- Гарантированные ошибки α и β
- Оптимальность — минимальное среднее число наблюдений
- Адаптивность — пороги под каждого клиента


## Результаты

| Метрика | Значение |
|--------|---------|
| Транзакций | 23 414 |
| Клиентов | 100 |
| Доля фрода | 3% |
| Алертов | 81 |
| Среднее время детекции | 21 460 часов |
| α (ошибка I рода) | 0.01 |
| β (ошибка II рода) | 0.001 |


## Как это работает

Гипотезы:
- H0 — транзакция честная (логнормальное распределение)
- H1 — транзакция мошенническая (логнормальное распределение)

Логарифм отношения правдоподобия:
log Λ = Σ [log f1(xi) - log f0(xi)]

Пороги Вальда:
A = log((1-β)/α) — верхний порог (принимаем H1)
B = log(β/(1-α)) — нижний порог (принимаем H0)

Решение:
- Если log Λ ≥ A → АЛЕРТ (мошенничество)
- Если log Λ ≤ B → транзакция честная
- Иначе → продолжаем наблюдение


## Архитектура проекта
sprt-fraud-detector/
├── data/
│ ├── clients.csv
│ ├── transactions_synthetic.csv
│ └── distribution_params.json
├── notebooks/
│ ├── 01_generate_data.ipynb
│ ├── 02_fit_distributions.ipynb
│ └── 03_visualization.ipynb
├── scripts/
│ ├── sprt_core.py
│ ├── simulate_stream.py
│ └── load_clients.py
├── sql/
│ ├── create_tables.sql
│ ├── sprt_functions.sql
│ └── triggers.sql
├── reports/
│ └── distributions_fitted.png
├── config.py
├── requirements.txt
└── README.md

## Технологии

| Компонент | Технология |
|-----------|------------|
| SPRT-ядро | Python + NumPy + SciPy |
| База данных | PostgreSQL |
| Визуализация | Plotly + Matplotlib |
| Аналитика | Pandas + Jupyter |

## Установка и запуск
git clone https://github.com/ayssin/sprt-fraud-detector.git
cd sprt-fraud-detector
pip install -r requirements.txt
jupyter notebook notebooks/01_generate_data.ipynb
python scripts/simulate_stream.py
jupyter notebook notebooks/03_visualization.ipynb

## Сравнение с методами

| Метод | Онлайн | Гарантированные ошибки | Адаптивность |
|-------|--------|----------------------|--------------|
| SPRT | Да | Да | Да |
| 3 сигмы | Да | Нет | Нет |
| ML-модель | Нет | Нет | Нет |
| Rule-based | Да | Нет | Нет |

## Лицензия

MIT © 2026
