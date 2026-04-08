from persistence import Activity, repo
import sys


def main(args):
    inputfilename = args[1]
    with open(inputfilename) as inputfile:
        for lineno, line in enumerate(inputfile, 1):
            line = line.strip()
            if not line:
                continue
            try:
                product_id_str, quantity_str, activator_id_str, date = map(str.strip, line.split(","))
                product_id = int(product_id_str)
                quantity = int(quantity_str)
                activator_id = int(activator_id_str)
            except ValueError as e:
                print(f"Line {lineno}: invalid format — {e}, skipping.")
                continue

            if quantity == 0:
                print(f"Line {lineno}: quantity is zero, skipping.")
                continue

            product = repo.products.find(id=product_id)
            if not product:
                print(f"Line {lineno}: product {product_id} not found, skipping.")
                continue

            if not repo.employees.find(id=activator_id) and not repo.suppliers.find(id=activator_id):
                print(f"Line {lineno}: activator {activator_id} not found in employees or suppliers, skipping.")
                continue

            product = product[0]
            if quantity > 0 or (quantity < 0 and product.quantity >= abs(quantity)):
                try:
                    repo.activities.insert(Activity(product_id, quantity, activator_id, date))
                    new_quantity = product.quantity + quantity
                    repo._conn.execute(
                        "UPDATE products SET quantity = ? WHERE id = ?",
                        (new_quantity, product_id)
                    )
                    repo._conn.commit()
                except Exception as e:
                    repo._conn.rollback()
                    print(f"Line {lineno}: transaction failed — {e}")


if __name__ == '__main__':
    main(sys.argv)
