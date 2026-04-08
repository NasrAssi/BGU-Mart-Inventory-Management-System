import sqlite3
import atexit
import os
from dbtools import Dao

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bgumart.db')


class Employee:
    def __init__(self, id, name, salary, branch_id):
        self.id = id
        self.name = name
        self.salary = salary
        self.branch_id = branch_id


class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Branch:
    _table_name = 'branches'

    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activity:
    _table_name = 'activities'

    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


class Repository:
    def __init__(self):
        self._conn = sqlite3.connect(_DB_PATH)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self.employees = Dao(Employee, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.products = Dao(Product, self._conn)
        self.branches = Dao(Branch, self._conn)
        self.activities = Dao(Activity, self._conn)

    def reinitialize(self):
        self._conn = sqlite3.connect(_DB_PATH)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self.employees = Dao(Employee, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.products = Dao(Product, self._conn)
        self.branches = Dao(Branch, self._conn)
        self.activities = Dao(Activity, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                branch_id INT REFERENCES branches(id)
            );

            CREATE TABLE suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_information TEXT
            );

            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                number_of_employees INTEGER
            );

            CREATE TABLE activities (
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                activator_id INTEGER NOT NULL,
                date TEXT NOT NULL
            );
        """)


repo = Repository()
atexit.register(repo._close)
