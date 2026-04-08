from persistence import Branch, Employee, Product, Supplier, repo, _DB_PATH
import sys
import os


def add_branch(splittedline):
    repo.branches.insert(Branch(int(splittedline[0]), splittedline[1], int(splittedline[2])))


def add_supplier(splittedline):
    repo.suppliers.insert(Supplier(int(splittedline[0]), splittedline[1], splittedline[2]))


def add_product(splittedline):
    repo.products.insert(Product(int(splittedline[0]), splittedline[1], float(splittedline[2]), int(splittedline[3])))


def add_employee(splittedline):
    repo.employees.insert(Employee(int(splittedline[0]), splittedline[1], float(splittedline[2]), int(splittedline[3])))


adders = {"B": add_branch, "S": add_supplier, "P": add_product, "E": add_employee}


def main(args):
    inputfilename = args[1]
    repo._close()
    if os.path.isfile(_DB_PATH):
        try:
            os.remove(_DB_PATH)
        except PermissionError as e:
            print(f"Cannot remove database file: {e}")
            sys.exit(1)
    repo.reinitialize()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for lineno, line in enumerate(inputfile, 1):
            line = line.strip()
            if not line:
                continue
            splittedline = line.split(",")
            adder = adders.get(splittedline[0])
            if adder:
                adder(splittedline[1:])
            else:
                print(f"Warning: unknown record type {splittedline[0]!r} on line {lineno}, skipping.")


if __name__ == '__main__':
    main(sys.argv)
