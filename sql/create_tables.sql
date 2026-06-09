DROP TABLE IF EXISTS sprt_alerts CASCADE;
DROP TABLE IF EXISTS sprt_state CASCADE;
DROP TABLE IF EXISTS sprt_params CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sprt_state (
    client_id INTEGER PRIMARY KEY,
    log_likelihood_ratio DOUBLE PRECISION DEFAULT 0.0
);

CREATE TABLE sprt_params (
    id SERIAL PRIMARY KEY,
    alpha DOUBLE PRECISION NOT NULL,
    beta DOUBLE PRECISION NOT NULL,
    a DOUBLE PRECISION NOT NULL,
    b DOUBLE PRECISION NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sprt_alerts (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    alert_type TEXT CHECK (alert_type IN ('fraud', 'normal')),
    log_likelihood_ratio DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sprt_params (alpha, beta, a, b)
VALUES (0.05, 0.1, (1-0.1)/0.05, 0.1/(1-0.05));