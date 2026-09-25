-- Group roles. Individual logins are created with create_staff_login() and
-- inherit one of these.
--   pharmacy_admin     full read/write on every table
--   pharmacy_employee  read everything except salaries, register patients,
--                      sell and restock only through the functions

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'pharmacy_admin') THEN
        CREATE ROLE pharmacy_admin NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'pharmacy_employee') THEN
        CREATE ROLE pharmacy_employee NOLOGIN;
    END IF;
END $$;

GRANT USAGE ON SCHEMA public TO pharmacy_admin, pharmacy_employee;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pharmacy_admin;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO pharmacy_admin;

GRANT SELECT ON pharmacy, doctor, medicine, patient, contains, associated_with, bill,
                stock_view, low_stock TO pharmacy_employee;
GRANT SELECT (eid, emp_name, address, sex, contact, store_id) ON employee TO pharmacy_employee;
GRANT INSERT (p_name, address, sex, contact, doc_id, store_id) ON patient TO pharmacy_employee;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO pharmacy_employee;

REVOKE ALL ON FUNCTION sell_medicine(INT, INT, INT, INT), add_stock(INT, INT, INT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION sell_medicine(INT, INT, INT, INT), add_stock(INT, INT, INT),
                          current_store() TO pharmacy_employee, pharmacy_admin;

-- Create a login for an employee (or an admin when p_eid is NULL).
CREATE OR REPLACE PROCEDURE create_staff_login(p_login NAME, p_password TEXT, p_eid INT DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L IN ROLE %I', p_login, p_password,
                   CASE WHEN p_eid IS NULL THEN 'pharmacy_admin' ELSE 'pharmacy_employee' END);
    IF p_eid IS NOT NULL THEN
        UPDATE employee SET db_role = p_login WHERE eid = p_eid;
    END IF;
END;
$$;
