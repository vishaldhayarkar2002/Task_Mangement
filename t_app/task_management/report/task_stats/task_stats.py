import frappe
from frappe.utils import nowdate
# File: task_management/report/task_stats/task_stats.py

def execute(filters=None):
    import frappe
    from datetime import datetime
    
    columns = [
        {"fieldname": "total_tasks", "label": "Total Tasks", "fieldtype": "Int", "width": 150},
        {"fieldname": "completed", "label": "Completed", "fieldtype": "Int", "width": 150},
        {"fieldname": "not_completed", "label": "Not Completed", "fieldtype": "Int", "width": 150},
        {"fieldname": "overdue", "label": "Overdue", "fieldtype": "Int", "width": 150},
    ]
    
    conditions = ""
    if filters.get("assigned_to"):
        conditions += f" AND assigned_to = '{filters['assigned_to']}'"
    if filters.get("status"):
        conditions += f" AND status = '{filters['status']}'"
    
    today = datetime.today().date()
    
    total_tasks = frappe.db.count("tsk", filters={"assigned_to": filters.get("assigned_to")})
    completed_tasks = frappe.db.count("tsk", filters={"status": "Completed", "assigned_to": filters.get("assigned_to")})
    not_completed_tasks = total_tasks - completed_tasks
    overdue_tasks = frappe.db.count("tsk", filters={"status": ["not in", ["Completed"]], "e_date": ["<", today], "assigned_to": filters.get("assigned_to")})
    
    data = [{
        "total_tasks": total_tasks,
        "completed": completed_tasks,
        "not_completed": not_completed_tasks,
        "overdue": overdue_tasks,
    }]
    
    return columns, data
