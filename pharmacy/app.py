"""Tkinter front end. All database work goes through pharmacy.db.Session."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .db import TABLES, PharmacyError, Session

SEXES = ("Male", "Female", "Other")


class TablePanel(ttk.Frame):
    """Search bar + results grid for one table or view, with an optional form."""

    WIDE = {"Name": 140, "Address": 170, "Medicine": 130, "Manufacturer": 140,
            "Date": 120, "Expires": 95}

    def __init__(self, master, session: Session, table: str, form_builder=None,
                 default_filter: tuple[str, object] | None = None, searchable: bool = True):
        super().__init__(master, padding=8)
        self.session, self.table = session, table
        self.default_filter = default_filter
        spec = TABLES[table]

        bar = ttk.Frame(self)
        bar.pack(fill="x")
        if spec.searchable and searchable:
            ttk.Label(bar, text="Search by").pack(side="left")
            self.column = ttk.Combobox(bar, values=spec.searchable, state="readonly", width=14)
            self.column.current(0)
            self.column.pack(side="left", padx=4)
            self.value = ttk.Entry(bar, width=22)
            self.value.pack(side="left", padx=4)
            self.value.bind("<Return>", lambda _e: self.search())
            ttk.Button(bar, text="Search", command=self.search).pack(side="left", padx=4)
        ttk.Button(bar, text="Show all", command=self.show_all).pack(side="left", padx=4)
        self.count = ttk.Label(bar, foreground="#555")
        self.count.pack(side="right")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, pady=(8, 0))
        self.tree = ttk.Treeview(body, columns=spec.columns, show="headings", height=14)
        for c in spec.columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=self.WIDE.get(c, max(60, 9 * len(c))), anchor="center")
        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")
        if form_builder:
            form = ttk.LabelFrame(body, text="Add", padding=8)
            form.pack(side="left", fill="y", padx=(10, 0))
            form_builder(form, self)
        self.show_all()

    def fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=["" if v is None else v for v in r])
        self.count.configure(text=f"{len(rows)} rows")

    def show_all(self):
        col, val = self.default_filter or (None, None)
        self._load(col, val)

    def search(self):
        self._load(self.column.get(), self.value.get())

    def _load(self, column, value):
        try:
            self.fill(self.session.rows(self.table, column, value))
        except PharmacyError as e:
            messagebox.showwarning("Search", str(e))


def form(parent, fields, submit_text, on_submit):
    """Build a labelled form. ``fields`` = [(label, kind)], kind 'entry' or a tuple of choices."""
    widgets = []
    for i, (label, kind) in enumerate(fields):
        ttk.Label(parent, text=label).grid(row=i, column=0, sticky="w", pady=3)
        if isinstance(kind, tuple):
            w = ttk.Combobox(parent, values=kind, state="readonly", width=18)
            w.current(0)
        else:
            w = ttk.Entry(parent, width=20)
        w.grid(row=i, column=1, pady=3)
        widgets.append(w)

    def submit():
        values = [w.get() for w in widgets]
        try:
            message = on_submit(*values)
        except PharmacyError as e:
            messagebox.showwarning(submit_text, str(e))
            return
        for w in widgets:
            if isinstance(w, ttk.Entry) and not isinstance(w, ttk.Combobox):
                w.delete(0, "end")
        messagebox.showinfo(submit_text, message)

    ttk.Button(parent, text=submit_text, command=submit).grid(
        row=len(fields), column=0, columnspan=2, pady=(10, 0), sticky="ew")


class MainWindow:
    def __init__(self, root: tk.Tk, session: Session):
        self.root, self.s = root, session
        role = "Admin" if session.is_admin else f"Store {session.store_id}"
        root.title(f"MedCare — {session.store_name()} ({session.user}, {role})")
        root.geometry("1100x560")
        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True)
        tabs = self.admin_tabs() if session.is_admin else self.employee_tabs()
        for title, panel in tabs:
            nb.add(panel(nb), text=title)

    # ---- employee -------------------------------------------------------
    def employee_tabs(self):
        s, store = self.s, self.s.store_id
        mine = ("store_id", store)

        def billing(frame, panel):
            def sell(pid, medicine, qty):
                bill = s.sell(pid, medicine, qty)
                panel.show_all()
                return f"Bill {bill[0]}: {bill[4]} × drug {bill[3]} = ₹{bill[5]}"
            form(frame, [("Patient ID", "entry"), ("Medicine (name or ID)", "entry"),
                         ("Quantity", "entry")], "Create bill", sell)

        def patients(frame, panel):
            def add(name, sex, contact, doc, address):
                pid = s.add_patient(name, sex, contact, doc, address)
                panel.show_all()
                return f"Patient registered with ID {pid}"
            form(frame, [("Name", "entry"), ("Sex", SEXES), ("Contact (10 digits)", "entry"),
                         ("Doctor ID", "entry"), ("Address", "entry")], "Register", add)

        def restock(frame, panel):
            def add(medicine, qty):
                new = s.add_stock(store, medicine, qty)
                panel.show_all()
                return f"Stock is now {new}"
            form(frame, [("Medicine (name or ID)", "entry"), ("Quantity to add", "entry")],
                 "Add stock", add)

        return [
            ("Billing", lambda nb: TablePanel(nb, s, "bill", billing, mine)),
            ("Stock", lambda nb: TablePanel(nb, s, "stock", restock, mine)),
            ("Patients", lambda nb: TablePanel(nb, s, "patient", patients, mine)),
            ("Staff", lambda nb: TablePanel(nb, s, "staff", None, mine)),
            ("Low stock", lambda nb: TablePanel(nb, s, "low_stock", None, mine)),
        ]

    # ---- admin ----------------------------------------------------------
    def admin_tabs(self):
        s = self.s

        def employees(frame, panel):
            def add(name, sex, contact, store, salary, address):
                eid = s.add_employee(name, sex, contact, store, salary, address)
                panel.show_all()
                return f"Employee added with ID {eid}"
            form(frame, [("Name", "entry"), ("Sex", SEXES), ("Contact", "entry"),
                         ("Store ID", "entry"), ("Salary", "entry"), ("Address", "entry")],
                 "Add employee", add)

        def restock(frame, panel):
            def add(store, medicine, qty):
                new = s.add_stock(store, medicine, qty)
                panel.show_all()
                return f"Stock is now {new}"
            form(frame, [("Store ID", "entry"), ("Medicine (name or ID)", "entry"),
                         ("Quantity to add", "entry")], "Add stock", add)

        def billing(frame, panel):
            def sell(store, pid, medicine, qty):
                bill = s.sell(pid, medicine, qty, store_id=store)
                panel.show_all()
                return f"Bill {bill[0]} created: ₹{bill[5]}"
            form(frame, [("Store ID", "entry"), ("Patient ID", "entry"),
                         ("Medicine (name or ID)", "entry"), ("Quantity", "entry")],
                 "Create bill", sell)

        return [
            ("Reports", lambda nb: ReportsPanel(nb, s)),
            ("Employees", lambda nb: TablePanel(nb, s, "employee", employees)),
            ("Patients", lambda nb: TablePanel(nb, s, "patient")),
            ("Doctors", lambda nb: TablePanel(nb, s, "doctor")),
            ("Stock", lambda nb: TablePanel(nb, s, "stock", restock)),
            ("Bills", lambda nb: TablePanel(nb, s, "bill", billing)),
        ]


class ReportsPanel(ttk.Frame):
    def __init__(self, master, session: Session):
        super().__init__(master, padding=8)
        reports = (("Sales by store", "sales_by_store", 0, 0),
                   ("Top medicines by revenue", "top_medicines", 0, 1),
                   ("Low stock (< 50 units, not expired)", "low_stock", 1, 0))
        for title, table, row, col in reports:
            box = ttk.LabelFrame(self, text=title, padding=4)
            box.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            panel = TablePanel(box, session, table, searchable=False)
            panel.tree.configure(height=7)
            panel.pack(fill="both", expand=True)
        self.columnconfigure((0, 1), weight=1, uniform="col")
        self.rowconfigure((0, 1), weight=1)


class LoginWindow:
    def __init__(self, root: tk.Tk, dbname: str, host: str):
        self.root, self.dbname, self.host = root, dbname, host
        root.title("MedCare Login")
        root.geometry("340x230")
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="MedCare", font=("", 16, "bold")).grid(columnspan=2, pady=(0, 12))
        ttk.Label(self.frame, text="Username").grid(row=1, column=0, sticky="w")
        self.user = ttk.Entry(self.frame, width=24)
        self.user.grid(row=1, column=1, pady=4)
        ttk.Label(self.frame, text="Password").grid(row=2, column=0, sticky="w")
        self.password = ttk.Entry(self.frame, show="•", width=24)
        self.password.grid(row=2, column=1, pady=4)
        self.password.bind("<Return>", lambda _e: self.login())
        self.status = ttk.Label(self.frame, foreground="red", wraplength=280)
        self.status.grid(row=3, columnspan=2, pady=4)
        ttk.Button(self.frame, text="Log in", command=self.login).grid(row=4, columnspan=2, sticky="ew")
        self.user.focus()

    def login(self):
        try:
            session = Session.login(self.user.get(), self.password.get(), self.dbname, self.host)
        except PharmacyError as e:
            self.status.configure(text=str(e))
            return
        self.frame.destroy()
        MainWindow(self.root, session)
