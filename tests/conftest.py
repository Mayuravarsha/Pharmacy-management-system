"""Fixtures that build a throw-away database from sql/*.sql.

Needs a PostgreSQL server and a superuser connection, taken from the usual
PG* environment variables (PGHOST, PGUSER, PGPASSWORD). Tests are skipped
if no server is reachable.
"""

import os
import subprocess
import uuid
from pathlib import Path

import psycopg
import pytest

from pharmacy.db import Session

ROOT = Path(__file__).resolve().parent.parent
HOST = os.environ.get("PGHOST", "localhost")
PASSWORD = "test-pass-123"


def _admin_conn(dbname="postgres"):
    return psycopg.connect(dbname=dbname, host=HOST, autocommit=True, connect_timeout=3)


@pytest.fixture(scope="session")
def database():
    try:
        _admin_conn().close()
    except psycopg.OperationalError as e:
        pytest.skip(f"PostgreSQL not available: {e}")
    name = f"pharmacy_test_{uuid.uuid4().hex[:8]}"
    subprocess.run([str(ROOT / "scripts" / "setup_db.sh"), name], check=True,
                   capture_output=True, env={**os.environ, "PGHOST": HOST})
    suffix = uuid.uuid4().hex[:6]
    logins = {"admin": f"admin_{suffix}", "employee": f"med_ramesh_{suffix}"}
    with _admin_conn(name) as conn:
        conn.execute("CALL create_staff_login(%s, %s)", (logins["admin"], PASSWORD))
        conn.execute("CALL create_staff_login(%s, %s, 1001)", (logins["employee"], PASSWORD))
    yield name, logins
    with _admin_conn() as conn:
        conn.execute(f'DROP DATABASE "{name}" WITH (FORCE)')
        for login in logins.values():
            conn.execute(f'DROP ROLE IF EXISTS "{login}"')


@pytest.fixture
def admin(database):
    name, logins = database
    s = Session.login(logins["admin"], PASSWORD, dbname=name, host=HOST)
    yield s
    s.close()


@pytest.fixture
def employee(database):
    name, logins = database
    s = Session.login(logins["employee"], PASSWORD, dbname=name, host=HOST)
    yield s
    s.close()


@pytest.fixture
def superuser(database):
    with _admin_conn(database[0]) as conn:
        yield conn
