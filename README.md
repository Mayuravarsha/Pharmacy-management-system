# Pharmacy Management System

A desktop app for running a chain of pharmacies, built for a database course at PES University (2022). It is written in Python with Tkinter and uses PostgreSQL for storage.

## Features

- Login with PostgreSQL roles. Users whose name starts with `med` get the employee view and everyone else gets the admin view
- Manage stores, employees, doctors, patients and medicines
- Billing that checks the stock of the store before a sale
- Add stock to a store
- Search any table by a chosen column or show all records

## Database design

The schema was designed from an ER diagram and has 8 tables. These are `pharmacy`, `employee`, `doctor`, `patient`, `medicine`, `bill`, `contains` (stock of each medicine per store) and `associated_with` (doctors linked to stores). The design is explained in `report_final.pdf`.

All values entered in the app are passed to PostgreSQL as query parameters and every change is committed straight after it runs.

## Running it

1. Install PostgreSQL and Python 3
2. Install the driver

   ```bash
   pip install psycopg2-binary
   ```

3. Create the database and load the sample data. The first script drops and recreates the `pharmacy_mang` database

   ```bash
   psql -U postgres -f pharmacy_mang_ddl.sql
   psql -U postgres -f pharmacy_mang_insert.sql
   ```

4. Create a PostgreSQL role to log in with and give it access to the tables. A role name starting with `med` opens the employee view.
5. Start the app

   ```bash
   python main.py
   ```

## Files

| File | Description |
| --- | --- |
| `main.py` | Tkinter app |
| `pharmacy_mang_ddl.sql` | Table definitions |
| `pharmacy_mang_insert.sql` | Sample data |
| `report_final.pdf` | ER diagram, relational schema and design notes |
