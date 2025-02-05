import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "assigned_to", "label": "Assigned To", "fieldtype": "Link", "options": "User", "width": 150},
        {"fieldname": "total_tasks", "label": "Total Tasks", "fieldtype": "Int", "width": 120},
        {"fieldname": "completed", "label": "Completed", "fieldtype": "Int", "width": 120},
        {"fieldname": "not_completed", "label": "Not Completed", "fieldtype": "Int", "width": 120},
        {"fieldname": "overdue", "label": "Overdue", "fieldtype": "Int", "width": 120}
    ]
    
    conditions = ""
    if filters.get("assigned_to"):
        conditions += f"AND assigned_to = '{filters.get('assigned_to')}' "
    
    data = frappe.db.sql(f'''
        SELECT assigned_to,
            COUNT(name) AS total_tasks,
            SUM(CASE WHEN status = "Completed" THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status != "Completed" THEN 1 ELSE 0 END) AS not_completed,
            SUM(CASE WHEN status != "Completed" AND e_date < CURDATE() THEN 1 ELSE 0 END) AS overdue
        FROM `tabtsk`
        WHERE 1=1 {conditions}
        GROUP BY assigned_to
    ''', as_dict=True)
    
    return columns, data
