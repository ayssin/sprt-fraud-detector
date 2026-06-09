CREATE OR REPLACE FUNCTION trg_transaction_sprt()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM update_sprt(NEW.client_id, NEW.amount);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS after_transaction_insert ON transactions;
CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
EXECUTE FUNCTION trg_transaction_sprt();

CREATE OR REPLACE FUNCTION trg_auto_recalc_thresholds()
RETURNS TRIGGER AS $$
BEGIN
    NEW.a := (1 - NEW.beta) / NEW.alpha;
    NEW.b := NEW.beta / (1 - NEW.alpha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_sprt_params_insert ON sprt_params;
CREATE TRIGGER before_sprt_params_insert
BEFORE INSERT ON sprt_params
FOR EACH ROW
EXECUTE FUNCTION trg_auto_recalc_thresholds();