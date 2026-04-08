# BGU Mart Inventory Management System

A lightweight, robust backend inventory management system built entirely in Python and SQLite. This project features a custom Object-Relational Mapping (ORM) layer, handling everything from database initialization to safe, transactional supply-chain updates.

## 🚀 Features

* **Custom ORM & DAO Pattern:** Utilizes Data Access Objects (`dbtools.py`, `persistence.py`) to abstract SQL queries and seamlessly map database rows to Python objects.
* **Data Initialization:** Parses structured text files (`config.txt`) to dynamically build and populate the database schema across multiple interrelated tables (Employees, Branches, Suppliers, Products).
* **Transactional Integrity:** Processes inventory activities (restocks and sales) sequentially. Uses SQL transactions and rollbacks to ensure data consistency, preventing negative inventory balances.
* **Automated Reporting:** Generates detailed, formatted reports on system state, employee sales performance, and a chronological log of all inventory activities.

## 🗂️ System Architecture

* **`dbtools.py`**: The core custom ORM engine. Contains the generic `Dao` class that dynamically constructs SQL `INSERT`, `SELECT`, and `DELETE` queries based on object attributes.
* **`persistence.py`**: Defines the data transfer objects (DTOs) and initializes the central `Repository` to manage connections and foreign key constraints.
* **`initiate.py`**: Wipes any existing state, creates a fresh SQLite database (`bgumart.db`), and seeds it using `config.txt`.
* **`action.py`**: The transaction processor. Reads sequential operations from `action.txt` and securely updates product quantities while logging activities.
* **`printdb.py`**: The reporting engine. Outputs the raw table states followed by synthesized employee performance and chronological activity reports.

## 🛠️ Usage

**Prerequisites:** Python 3.x installed on your system. No external libraries are required.

**1. Initialize the Database**
Build the database and populate it with initial data from the config file:
```bash
python initiate.py config.txt