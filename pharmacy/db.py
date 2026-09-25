"""Data access layer.

Every query the GUI needs lives here, so it can be tested without a window.
Column names that come from the UI (search fields) are checked against a
whitelist and quoted with psycopg's ``sql.Identifier``; values are always
passed as query parameters.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import psycopg
from psycopg import sql

DEFAULT_DB = os.environ.get("PHARMACY_DB", "pharmacy")
DEFAULT_HOST = os.environ.get("PGHOST", "localhost")


@dataclass(frozen=True)
class TableSpec:
    """How a table (or view) is shown in the app."""
    query: str                  # base SELECT; searches add "WHERE <col> = %s"
    columns: tuple[str, ...]    # headings, in SELECT order
    searchable: tuple[str, ...] # columns the user may search by


TABLES: dict[str, TableSpec] = {
    "patient": TableSpec(
        "SELECT pid, p_name, address, sex, contact, doc_id, store_id FROM patient",
        ("PID", "Name", "Address", "Sex", "Contact", "Doctor", "Store"),
        ("pid", "p_name", "contact", "doc_id", "store_id", "sex")),
    "employee": TableSpec(
        "SELECT eid, emp_name, address, sex, salary, contact, store_id FROM employee",
        ("ID", "Name", "Address", "Sex", "Salary", "Contact", "Store"),
        ("eid", "emp_name", "store_id", "sex")),
    "staff": TableSpec(  # employee view without salaries
        "SELECT eid, emp_name, address, sex, contact, store_id FROM employee",
        ("ID", "Name", "Address", "Sex", "Contact", "Store"),
        ("eid", "emp_name", "store_id")),
    "doctor": TableSpec(
        "SELECT d.doc_id, d.doc_name, d.address, d.contact, d.hospital, a.store_id "
        "FROM doctor d JOIN associated_with a USING (doc_id)",
        ("ID", "Name", "Address", "Contact", "Hospital", "Store"),
        ("doc_id", "doc_name", "hospital", "store_id")),
    "stock": TableSpec(
        "SELECT drug_id, drug_name, manufacturer, price, quantity, exp_date, store_id FROM stock_view",
        ("ID", "Medicine", "Manufacturer", "Price", "Qty", "Expires", "Store"),
        ("drug_id", "drug_name", "manufacturer", "store_id")),
    "bill": TableSpec(
        "SELECT bill_id, pid, doc_id, drug_id, quantity, amount, store_id, "
        "to_char(billed_at, 'YYYY-MM-DD HH24:MI') FROM bill",
        ("Bill", "PID", "Doctor", "Drug", "Qty", "Amount", "Store", "Date"),
        ("bill_id", "pid", "store_id", "drug_id")),
    "low_stock": TableSpec(
        "SELECT store_id, drug_name, quantity, exp_date FROM low_stock",
        ("Store", "Medicine", "Qty", "Expires"), ("store_id",)),
    "sales_by_store": TableSpec(
        "SELECT store_id, store_name, bills, units_sold, revenue FROM sales_by_store",
        ("Store", "Name", "Bills", "Units", "Revenue"), ("store_id",)),
    "top_medicines": TableSpec(
        "SELECT revenue_rank, drug_name, units_sold, revenue FROM top_medicines",
        ("Rank", "Medicine", "Units", "Revenue"), ()),
}


class PharmacyError(Exception):
    """A user-facing error (bad input, not enough stock, no permission...)."""


class Session:
    """A logged-in user: an admin, or an employee tied to one store."""

    def __init__(self, conn: psycopg.Connection):
        self.conn = conn
        with conn.cursor() as cur:
            cur.execute("SELECT session_user, pg_has_role(session_user, 'pharmacy_admin', 'member'), "
                        "current_store()")
            self.user, self.is_admin, self.store_id = cur.fetchone()
        if not self.is_admin and self.store_id is None:
            raise PharmacyError(f"login '{self.user}' is not linked to an employee record")

    @classmethod
    def login(cls, user: str, password: str, dbname: str = DEFAULT_DB,
              host: str = DEFAULT_HOST) -> "Session":
        if not user or not password:
            raise PharmacyError("enter a username and password")
        try:
            conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host,
                                   autocommit=True, connect_timeout=5)
        except psycopg.OperationalError as e:
            raise PharmacyError("wrong username or password, or the database is not running") from e
        return cls(conn)

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------ queries
    def _run(self, query, params=()):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall() if cur.description else None
        except psycopg.errors.InsufficientPrivilege as e:
            raise PharmacyError("you do not have permission to do that") from e
        except (psycopg.errors.CheckViolation, psycopg.errors.ForeignKeyViolation,
                psycopg.errors.NotNullViolation, psycopg.errors.InvalidTextRepresentation,
                psycopg.errors.RaiseException) as e:
            raise PharmacyError(e.diag.message_primary or str(e)) from e

    def rows(self, table: str, column: str | None = None, value=None) -> list[tuple]:
        """All rows of a table/view, or those where ``column`` equals ``value``."""
        spec = TABLES[table]
        query = sql.SQL(spec.query)
        params: tuple = ()
        if column:
            if column not in spec.searchable:
                raise PharmacyError(f"cannot search {table} by {column}")
            if value in (None, ""):
                raise PharmacyError("enter a value to search for")
            if column.endswith("name") or column in ("manufacturer", "hospital"):
                query += sql.SQL(" WHERE lower({}::text) LIKE lower(%s)").format(sql.Identifier(column))
                params = (f"%{value}%",)
            else:
                query += sql.SQL(" WHERE {}::text = %s").format(sql.Identifier(column))
                params = (str(value),)
        query += sql.SQL(" ORDER BY 1")
        return self._run(query, params)

    def medicine_id(self, name_or_id: str) -> int:
        if str(name_or_id).strip().isdigit():
            return int(name_or_id)
        found = self._run("SELECT drug_id FROM medicine WHERE lower(drug_name) = lower(%s)",
                          (name_or_id.strip(),))
        if not found:
            raise PharmacyError(f"no medicine called '{name_or_id}'")
        return found[0][0]

    # ------------------------------------------------------------ changes
    def add_patient(self, name, sex, contact, doc_id, address, store_id=None) -> int:
        store = store_id if self.is_admin else self.store_id
        return self._run(
            "INSERT INTO patient (p_name, sex, contact, doc_id, address, store_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING pid",
            (name.strip(), sex, contact.strip(), _int(doc_id, "doctor ID"), address.strip(), store))[0][0]

    def add_employee(self, name, sex, contact, store_id, salary, address) -> int:
        return self._run(
            "INSERT INTO employee (emp_name, sex, contact, store_id, salary, address) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING eid",
            (name.strip(), sex, contact.strip(), _int(store_id, "store ID"),
             _number(salary, "salary"), address.strip()))[0][0]

    def sell(self, pid, medicine, quantity, store_id=None) -> tuple:
        """Create a bill through sell_medicine(); returns the bill row."""
        store = _int(store_id, "store ID") if self.is_admin else self.store_id
        bill_id = self._run("SELECT sell_medicine(%s, %s, %s, %s)",
                            (_int(pid, "patient ID"), self.medicine_id(medicine),
                             _int(quantity, "quantity"), store))[0][0]
        return self.rows("bill", "bill_id", bill_id)[0]

    def add_stock(self, store_id, medicine, quantity) -> int:
        store = _int(store_id, "store ID") if self.is_admin else self.store_id
        return self._run("SELECT add_stock(%s, %s, %s)",
                         (store, self.medicine_id(medicine), _int(quantity, "quantity")))[0][0]

    def store_name(self) -> str:
        if self.store_id is None:
            return "All stores"
        return self._run("SELECT store_name FROM pharmacy WHERE store_id = %s", (self.store_id,))[0][0]


def _int(value, what: str) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        raise PharmacyError(f"{what} must be a whole number") from None


def _number(value, what: str) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        raise PharmacyError(f"{what} must be a number") from None
