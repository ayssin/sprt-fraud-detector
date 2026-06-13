<div align="center">
  
# 🚨 SPRT Fraud Detector
  
**Последовательный анализ Вальда для детекции мошеннических транзакций в реальном времени**
  
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  
*Онлайн-детектор с гарантированными вероятностями ошибок I и II рода*
  
</div>

---

## 📊 О проекте

**SPRT Fraud Detector** — реализация последовательного анализа Вальда (Sequential Probability Ratio Test) для обнаружения мошеннических транзакций. В отличие от классических ML-моделей, SPRT анализирует каждую транзакцию моментально и принимает решение, накопил ли алгоритм достаточно статистических доказательств.

### 🎯 Ключевые особенности

| Особенность | Описание |
|-------------|----------|
| ⚡ Онлайн-режим | Решение принимается после каждой транзакции |
| 📊 Гарантированные ошибки | α и β задаются явно |
| 🧠 Оптимальность | Минимальное среднее число наблюдений |
| 🔄 Адаптивность | Пороги пересчитываются под каждого клиента |

---

## 📈 Результаты

| Метрика | Значение |
|:--------|---------:|
| 📦 Транзакций | 23 414 |
| 👥 Клиентов | 100 |
| 💀 Доля фрода | 3% |
| 🚨 Алертов | 81 |
| ⏱️ Среднее время детекции | 21 460 часов |
| 📊 α (ошибка I рода) | 0.01 |
| 📊 β (ошибка II рода) | 0.001 |

---

## 🧠 Как это работает

### Гипотезы

| Гипотеза | Описание | Распределение |
|----------|----------|---------------|
| **H₀** | Транзакция честная | Логнормальное (μ₀, σ₀) |
| **H₁** | Транзакция мошенническая | Логнормальное (μ₁, σ₁) |

### Формулы

| Параметр | Формула |
|----------|---------|
| Логарифм отношения правдоподобия | `log Λ = Σ [log f₁(xᵢ) - log f₀(xᵢ)]` |
| Верхний порог | `A = log((1-β)/α)` — принимаем H₁ |
| Нижний порог | `B = log(β/(1-α))` — принимаем H₀ |

### Правило принятия решений

| Условие | Решение |
|---------|---------|
| `log Λ ≥ A` | 🚨 **АЛЕРТ! Мошенничество** |
| `log Λ ≤ B` | ✅ Транзакция честная |
| `B < log Λ < A` | ⏳ Продолжаем наблюдение |

---

## 📁 Архитектура проекта
sprt-fraud-detector/
├── 📂 data/
│ ├── clients.csv
│ ├── transactions_synthetic.csv
│ └── distribution_params.json
├── 📂 notebooks/
│ ├── 01_generate_data.ipynb
│ ├── 02_fit_distributions.ipynb
│ └── 03_visualization.ipynb
├── 📂 scripts/
│ ├── sprt_core.py
│ ├── simulate_stream.py
│ └── load_clients.py
├── 📂 sql/
│ ├── create_tables.sql
│ ├── sprt_functions.sql
│ └── triggers.sql
├── 📂 reports/
│ └── distributions_fitted.png
├── ⚙️ config.py
├── 📋 requirements.txt
└── 📖 README.md


---

## 🛠️ Технологии

| Компонент | Технология | Значок |
|-----------|------------|--------|
| SPRT-ядро | Python + NumPy + SciPy | 🐍 |
| База данных | PostgreSQL | 🐘 |
| Визуализация | Plotly + Matplotlib | 📊 |
| Аналитика | Pandas + Jupyter | 📓 |

---

## 🚀 Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ayssin/sprt-fraud-detector.git
cd sprt-fraud-detector
pip install -r requirements.txt
jupyter notebook notebooks/01_generate_data.ipynb
python scripts/simulate_stream.py
jupyter notebook notebooks/03_visualization.ipynb

📄 Лицензия
MIT © 2026 — свободное использование, копирование, модификация.

<div align="center">
⭐ Поставьте звезду репозиторию, если проект зашёл
</div> ```