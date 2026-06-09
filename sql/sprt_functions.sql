CREATE OR REPLACE FUNCTION update_sprt(
    p_client_id INTEGER,
    p_amount DECIMAL
)
RETURNS VOID AS $$
DECLARE
    current_lr DOUBLE PRECISION;
    A_val DOUBLE PRECISION;
    B_val DOUBLE PRECISION;
    new_lr DOUBLE PRECISION;
BEGIN
    SELECT log_likelihood_ratio INTO current_lr
    FROM sprt_state
    WHERE client_id = p_client_id;
    
    IF current_lr IS NULL THEN
        current_lr := 0.0;
        INSERT INTO sprt_state (client_id, log_likelihood_ratio)
        VALUES (p_client_id, 0.0);
    END IF;
    
    SELECT a, b INTO A_val, B_val
    FROM sprt_params
    ORDER BY id DESC LIMIT 1;
    
    IF p_amount > 100 THEN
        new_lr := current_lr + ln(1.2);
    ELSE
        new_lr := current_lr + ln(0.8);
    END IF;
    
    UPDATE sprt_state
    SET log_likelihood_ratio = new_lr
    WHERE client_id = p_client_id;
    
    IF new_lr >= A_val THEN
        INSERT INTO sprt_alerts (client_id, alert_type, log_likelihood_ratio)
        VALUES (p_client_id, 'fraud', new_lr);
        UPDATE sprt_state SET log_likelihood_ratio = 0.0
        WHERE client_id = p_client_id;
    ELSIF new_lr <= B_val THEN
        INSERT INTO sprt_alerts (client_id, alert_type, log_likelihood_ratio)
        VALUES (p_client_id, 'normal', new_lr);
        UPDATE sprt_state SET log_likelihood_ratio = 0.0
        WHERE client_id = p_client_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION recalc_thresholds(
    p_alpha DOUBLE PRECISION,
    p_beta DOUBLE PRECISION
)
RETURNS VOID AS $$
DECLARE
    new_A DOUBLE PRECISION;
    new_B DOUBLE PRECISION;
BEGIN
    new_A := (1 - p_beta) / p_alpha;
    new_B := p_beta / (1 - p_alpha);
    
    INSERT INTO sprt_params (alpha, beta, a, b)
    VALUES (p_alpha, p_beta, new_A, new_B);
END;
$$ LANGUAGE plpgsql;