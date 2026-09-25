-- Business logic that must be atomic lives in the database, so every
-- client (the Tkinter app, psql, tests) gets the same rules.

BEGIN;

-- Store of the employee who is logged in (NULL for admins).
CREATE OR REPLACE FUNCTION current_store() RETURNS INT
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public AS $$
    SELECT store_id FROM employee WHERE db_role = session_user
$$;

-- Sell ``p_qty`` units of a medicine to a patient from one store.
--   * locks the stock row, so two tills selling the last units cannot both succeed
--   * refuses expired medicine and quantities above the stock
--   * the price comes from the medicine table, not from the client
--   * the prescribing doctor is the patient's registered doctor
-- Returns the new bill_id.
CREATE OR REPLACE FUNCTION sell_medicine(p_pid INT, p_drug_id INT, p_qty INT, p_store_id INT)
RETURNS INT
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE
    v_stock   INT;
    v_price   NUMERIC;
    v_expiry  DATE;
    v_doc     INT;
    v_bill    INT;
BEGIN
    IF p_qty IS NULL OR p_qty <= 0 THEN
        RAISE EXCEPTION 'quantity must be positive' USING ERRCODE = 'check_violation';
    END IF;

    SELECT doc_id INTO v_doc FROM patient WHERE pid = p_pid;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'patient % does not exist', p_pid USING ERRCODE = 'foreign_key_violation';
    END IF;

    SELECT price, exp_date INTO v_price, v_expiry FROM medicine WHERE drug_id = p_drug_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'medicine % does not exist', p_drug_id USING ERRCODE = 'foreign_key_violation';
    END IF;
    IF v_expiry < current_date THEN
        RAISE EXCEPTION 'medicine % expired on %', p_drug_id, v_expiry USING ERRCODE = 'check_violation';
    END IF;

    SELECT quantity INTO v_stock FROM contains
     WHERE drug_id = p_drug_id AND store_id = p_store_id
       FOR UPDATE;
    IF NOT FOUND OR v_stock < p_qty THEN
        RAISE EXCEPTION 'only % in stock at store %', coalesce(v_stock, 0), p_store_id
              USING ERRCODE = 'check_violation';
    END IF;

    UPDATE contains SET quantity = quantity - p_qty
     WHERE drug_id = p_drug_id AND store_id = p_store_id;

    INSERT INTO bill (pid, doc_id, drug_id, quantity, amount, store_id, eid)
    VALUES (p_pid, v_doc, p_drug_id, p_qty, round(v_price * p_qty, 2), p_store_id,
            (SELECT eid FROM employee WHERE db_role = session_user))
    RETURNING bill_id INTO v_bill;
    RETURN v_bill;
END;
$$;

-- Add stock; creates the row if the store did not carry the medicine yet.
CREATE OR REPLACE FUNCTION add_stock(p_store_id INT, p_drug_id INT, p_qty INT)
RETURNS INT
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE
    v_new INT;
BEGIN
    IF p_qty IS NULL OR p_qty <= 0 THEN
        RAISE EXCEPTION 'quantity must be positive' USING ERRCODE = 'check_violation';
    END IF;
    INSERT INTO contains AS c (drug_id, store_id, quantity)
    VALUES (p_drug_id, p_store_id, p_qty)
    ON CONFLICT (drug_id, store_id) DO UPDATE SET quantity = c.quantity + EXCLUDED.quantity
    RETURNING quantity INTO v_new;
    RETURN v_new;
END;
$$;

-- Reporting views -----------------------------------------------------------

CREATE OR REPLACE VIEW stock_view AS
SELECT c.store_id, p.store_name, m.drug_id, m.drug_name, m.manufacturer,
       m.price, c.quantity, m.exp_date,
       m.exp_date < current_date                  AS expired,
       m.exp_date < current_date + 30             AS expires_within_30_days
  FROM contains c
  JOIN medicine m USING (drug_id)
  JOIN pharmacy p USING (store_id);

CREATE OR REPLACE VIEW low_stock AS
SELECT * FROM stock_view WHERE quantity < 50 AND NOT expired;

CREATE OR REPLACE VIEW sales_by_store AS
SELECT p.store_id, p.store_name,
       count(b.bill_id)              AS bills,
       coalesce(sum(b.quantity), 0)  AS units_sold,
       coalesce(sum(b.amount), 0)    AS revenue
  FROM pharmacy p
  LEFT JOIN bill b USING (store_id)
 GROUP BY p.store_id, p.store_name;

CREATE OR REPLACE VIEW top_medicines AS
SELECT m.drug_id, m.drug_name,
       sum(b.quantity) AS units_sold,
       sum(b.amount)   AS revenue,
       rank() OVER (ORDER BY sum(b.amount) DESC) AS revenue_rank
  FROM bill b
  JOIN medicine m USING (drug_id)
 GROUP BY m.drug_id, m.drug_name;

COMMIT;
