from persistence import repo


def main():
    # Load all data once — shared by both raw dumps and reports
    all_employees = repo.employees.find_all()
    all_suppliers = repo.suppliers.find_all()
    all_products = repo.products.find_all()
    all_branches = repo.branches.find_all()
    all_activities = repo.activities.find_all()

    products_by_id = {p.id: p for p in all_products}
    employees_by_id = {e.id: e for e in all_employees}
    suppliers_by_id = {s.id: s for s in all_suppliers}
    branches_by_id = {b.id: b.location for b in all_branches}

    activities_by_activator = {}
    for activity in all_activities:
        activities_by_activator.setdefault(activity.activator_id, []).append(activity)

    # Raw table dumps
    print("Activities")
    print('\n'.join(
        f"({a.product_id}, {a.quantity}, {a.activator_id}, '{a.date}')"
        for a in all_activities
    ) + '\n')

    print("Branches")
    print('\n'.join(
        f"({b.id}, '{b.location}', {b.number_of_employees})"
        for b in all_branches
    ) + '\n')

    print("Employees")
    print('\n'.join(
        f"({e.id}, '{e.name}', {e.salary}, {e.branch_id})"
        for e in all_employees
    ) + '\n')

    print("Products")
    print('\n'.join(
        f"({p.id}, '{p.description}', {p.price}, {p.quantity})"
        for p in all_products
    ) + '\n')

    print("Suppliers")
    print('\n'.join(
        f"({s.id}, '{s.name}', '{s.contact_information}')"
        for s in all_suppliers
    ) + '\n')

    # Employees report
    print("\nEmployees report")
    lines = []
    for row in sorted(all_employees, key=lambda e: e.name):
        total_sales = sum(
            activity.quantity * products_by_id[activity.product_id].price
            for activity in activities_by_activator.get(row.id, [])
            if activity.quantity < 0
        )
        branch_location = branches_by_id.get(row.branch_id, 'Unknown')
        lines.append(f"{row.name} {row.salary} {branch_location} {total_sales}")
    print('\n'.join(lines) + '\n')

    # Activities report
    print("\nActivities report")
    lines = []
    for activity in sorted(all_activities, key=lambda a: a.date):
        product = products_by_id.get(activity.product_id)
        if not product:
            continue
        actor_name = None
        supplier_name = None
        employee = employees_by_id.get(activity.activator_id)
        if employee:
            actor_name = employee.name
        else:
            supplier = suppliers_by_id.get(activity.activator_id)
            if supplier:
                supplier_name = supplier.contact_information
        lines.append(
            f"('{activity.date}', '{product.description}', {activity.quantity}, "
            f"{actor_name}, {supplier_name})"
        )
    print('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
