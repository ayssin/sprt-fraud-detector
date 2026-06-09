-- Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY,
    client_name TEXT
);

-- Таблица транзакций
CREATE TABLE IF NOT EXISTS transactions (
    txn_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(client_id),
    amount DECIMAL(10,2),
    txn_time TIMESTAMP,
    is_fraud BOOLEAN
);

-- Таблица состояния SPRT
CREATE TABLE IF NOT EXISTS sprt_state (
    client_id INTEGER PRIMARY KEY REFERENCES clients(client_id),
    log_lr DOUBLE PRECISION DEFAULT 0,
    last_txn_id INTEGER,
    alert_flag BOOLEAN DEFAULT FALSE
);

-- Таблица алертов
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(client_id),
    txn_id INTEGER REFERENCES transactions(txn_id),
    alert_time TIMESTAMP,
    log_lr_value DOUBLE PRECISION
);

-- Таблица параметров SPRT
CREATE TABLE IF NOT EXISTS sprt_params (
    param_name VARCHAR(50) PRIMARY KEY,
    param_value DOUBLE PRECISION,
    description TEXT
);

-- Таблица истории SPRT
CREATE TABLE IF NOT EXISTS sprt_history (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(client_id),
    txn_id INTEGER REFERENCES transactions(txn_id),
    log_lr DOUBLE PRECISION,
    txn_time TIMESTAMP
);