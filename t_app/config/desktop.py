from frappe import _

def get_data():
    return [
        {
            "module_name": "Task Management",
            "type": "module",
            "label": _( "Task Management")
        },
        {
            "label": _( "Task Reports"),
            "icon": "fa fa-list",
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Task Report",
                    "doctype": "tsk",
                    "description": _( "View task completion stats and overdue tasks."),
                    "onboard": 1
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Task Stats",
                    "doctype": "tsk",
                    "description": _( "Detailed Task Statistics including total, completed, not completed, and overdue tasks."),
                    "onboard": 1
                }
            ]
        }
    ]
