"""Start the app:  python -m pharmacy [--db pharmacy] [--host localhost]"""

import argparse
import tkinter as tk

from .app import LoginWindow
from .db import DEFAULT_DB, DEFAULT_HOST


def main() -> None:
    p = argparse.ArgumentParser(prog="pharmacy")
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--host", default=DEFAULT_HOST)
    args = p.parse_args()
    root = tk.Tk()
    LoginWindow(root, args.db, args.host)
    root.mainloop()


if __name__ == "__main__":
    main()
