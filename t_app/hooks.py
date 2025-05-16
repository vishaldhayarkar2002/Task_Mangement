app_name = "t_app"
app_title = "Task Management"
app_publisher = "vishal"
app_description = "To assign and createa tasks"
app_email = "abc@gmail.com"
app_license = "MIT"

app_include_css = "/assets/t_app/css/output.css"
app_include_js = "/assets/t_app/js/custom_pos.js"

doc_events = {
    "tsk": {
        "after_insert": "t_app.task_management.doctype.tsk.tsk.notify_user_on_assignment",
        "on_update": [
            "t_app.task_management.doctype.tsk.tsk.notify_user_on_status_change",
            "t_app.task_management.doctype.tsk.tsk.notify_creator_on_completion"
        ]
    }
}

report_whitelist = [
    'task_completion_stats'
]
