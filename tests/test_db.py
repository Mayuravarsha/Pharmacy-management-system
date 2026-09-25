import threading

import psycopg
import pytest

from pharmacy.db import PharmacyError, Session

from .conftest import HOST, PASSWORD


def stock(conn, store, drug):
    return conn.execute("SELECT quantity FROM contains WHERE store_id=%s AND drug_id=%s",
                        (store, drug)).fetchone()[0]


# --------------------------------------------------------------- login / roles
def test_roles_are_detected(admin, employee):
    assert admin.is_admin and admin.store_id is None
    assert not employee.is_admin and employee.store_id == 1
    assert employee.store_name() == "PESUMEDcare MysoreRoad"


def test_wrong_password(database):
    name, logins = database
    with pytest.raises(PharmacyError, match="wrong username or password"):
        Session.login(logins["admin"], "nope", dbname=name, host=HOST)


def test_employee_cannot_see_salaries(employee):
    with pytest.raises(PharmacyError, match="permission"):
        employee.rows("employee")
    assert len(employee.rows("staff")) == 8


def test_employee_cannot_change_stock_directly(employee):
    with pytest.raises(PharmacyError, match="permission"):
        employee._run("UPDATE contains SET quantity = 0")


# --------------------------------------------------------------------- inserts
def test_add_patient_gets_generated_id_and_employee_store(employee, superuser):
    pid = employee.add_patient("Asha K", "Female", "9876543210", 20178, "Jayanagar")
    row = superuser.execute("SELECT p_name, store_id FROM patient WHERE pid=%s", (pid,)).fetchone()
    assert pid > 3010 and row == ("Asha K", 1)


def test_add_patient_validation(employee):
    with pytest.raises(PharmacyError):
        employee.add_patient("Bad Phone", "Male", "12345", 20178, "x")
    with pytest.raises(PharmacyError):
        employee.add_patient("No Doctor", "Male", "9876543210", 99999, "x")
    with pytest.raises(PharmacyError, match="whole number"):
        employee.add_patient("Typo", "Male", "9876543210", "abc", "x")


def test_admin_adds_employee(admin):
    eid = admin.add_employee("New Hire", "Other", "9123456780", 2, "7000", "HAL")
    assert admin.rows("employee", "eid", eid)[0][1] == "New Hire"
    with pytest.raises(PharmacyError):
        admin.add_employee("Neg Salary", "Male", "9123456780", 2, "-5", "x")


# --------------------------------------------------------------------- billing
def test_sale_decrements_stock_and_prices_from_medicine(employee, superuser):
    before = stock(superuser, 1, 6072)
    bill = employee.sell(3001, "zyloprim", 4)
    bill_id, pid, doc_id, drug_id, qty, amount, store = bill[:7]
    assert (pid, doc_id, drug_id, qty, store) == (3001, 20178, 6072, 4, 1)
    assert float(amount) == pytest.approx(4 * 7.5)
    assert stock(superuser, 1, 6072) == before - 4


def test_employee_always_sells_from_own_store(employee, superuser):
    before = stock(superuser, 2, 6075)
    employee.sell(3002, 6075, 1, store_id=2)          # store_id ignored for employees
    assert stock(superuser, 2, 6075) == before


def test_cannot_oversell(employee, superuser):
    available = stock(superuser, 1, 6079)
    with pytest.raises(PharmacyError, match="in stock"):
        employee.sell(3001, 6079, available + 1)
    assert stock(superuser, 1, 6079) == available


def test_selling_last_unit_keeps_row_at_zero(admin, superuser):
    superuser.execute("UPDATE contains SET quantity = 2 WHERE store_id = 3 AND drug_id = 6083")
    admin.sell(3007, 6083, 2, store_id=3)
    assert stock(superuser, 3, 6083) == 0
    assert admin.add_stock(3, 6083, 10) == 10          # restock works afterwards


def test_expired_medicine_is_refused(admin):
    with pytest.raises(PharmacyError, match="expired"):
        admin.sell(3007, "Ogen", 1, store_id=3)


def test_medicine_not_carried_by_store(employee):
    with pytest.raises(PharmacyError, match="in stock"):
        employee.sell(3001, "Lotrel", 1)                # store 1 has no Lotrel row


def test_unknown_patient_and_medicine(employee):
    with pytest.raises(PharmacyError, match="patient"):
        employee.sell(1, 6072, 1)
    with pytest.raises(PharmacyError, match="no medicine"):
        employee.sell(3001, "Unobtainium", 1)
    with pytest.raises(PharmacyError, match="positive"):
        employee.sell(3001, 6072, 0)


def test_concurrent_sales_of_last_units(database, superuser):
    """Two tills sell the last 3 units at once: exactly one sale may succeed."""
    name, logins = database
    superuser.execute("UPDATE contains SET quantity = 3 WHERE store_id = 1 AND drug_id = 6074")
    barrier, results = threading.Barrier(2), []

    def till():
        s = Session.login(logins["employee"], PASSWORD, dbname=name, host=HOST)
        barrier.wait()
        try:
            s.sell(3001, 6074, 3)
            results.append("sold")
        except PharmacyError:
            results.append("refused")
        finally:
            s.close()

    threads = [threading.Thread(target=till) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == ["refused", "sold"]
    assert stock(superuser, 1, 6074) == 0


# ---------------------------------------------------------------- stock/search
def test_add_stock_creates_missing_row(admin, superuser):
    assert admin.add_stock(1, "Ogen", 5) == 5
    assert admin.add_stock(1, "Ogen", 5) == 10
    with pytest.raises(PharmacyError):
        admin.add_stock(1, "Ogen", -1)


def test_search_whitelist_blocks_injection(admin):
    with pytest.raises(PharmacyError, match="cannot search"):
        admin.rows("patient", "pid; DROP TABLE patient; --", "1")
    assert admin.rows("patient", "p_name", "' OR 1=1 --") == []


def test_name_search_is_case_insensitive_substring(admin):
    names = {r[1] for r in admin.rows("patient", "p_name", "sav")}
    assert names == {"Savithri S", "Savitha D"}


def test_reports(admin):
    sales = {r[0]: r for r in admin.rows("sales_by_store")}
    assert set(sales) == {1, 2, 3}
    top = admin.rows("top_medicines")
    assert top[0][0] == 1 and top[0][1] == "Hyzaar"
    assert all(r[2] < 50 for r in admin.rows("low_stock"))


def test_view_hides_nothing_it_should_not(employee):
    # employees can read the stock view and bills for reporting
    assert employee.rows("stock", "store_id", 1)
    assert employee.rows("bill", "store_id", 1)


def test_db_rejects_bad_dates(superuser):
    with pytest.raises(psycopg.errors.CheckViolation):
        superuser.execute("INSERT INTO medicine (drug_name, mfg_date, exp_date, price, manufacturer) "
                          "VALUES ('Backwards', '2024-01-02', '2024-01-01', 1, 'x')")
