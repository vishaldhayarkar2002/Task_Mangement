import frappe
from frappe.utils import today

def execute(filters=None):
    columns = [
        {"label": "User / Team", "fieldname": "assigned_to", "fieldtype": "Link", "options": "User"},
        {"label": "Total Tasks", "fieldname": "total_tasks", "fieldtype": "Int"},
        {"label": "Completed", "fieldname": "completed_tasks", "fieldtype": "Int"},
        {"label": "Not Completed", "fieldname": "not_completed", "fieldtype": "Int"},
        {"label": "Overdue", "fieldname": "overdue_tasks", "fieldtype": "Int"},
    ]
    
    conditions = ""
    if filters.get("assigned_to"):
        conditions += f"AND assigned_to = '{filters.get('assigned_to')}'"
    if filters.get("user_group"):
        conditions += f"AND user_group = '{filters.get('user_group')}'"
    
    query = f'''
        SELECT assigned_to,
            COUNT(name) AS total_tasks,
            SUM(CASE WHEN status = "Completed" THEN 1 ELSE 0 END) AS completed_tasks,
            SUM(CASE WHEN status != "Completed" THEN 1 ELSE 0 END) AS not_completed,
            SUM(CASE WHEN status != "Completed" AND e_date < '{today()}' THEN 1 ELSE 0 END) AS overdue_tasks
        FROM `tabtsk`
        WHERE assigned_to IS NOT NULL {conditions}
        GROUP BY assigned_to
    '''
    
    data = frappe.db.sql(query, as_dict=True)
    return columns, data
