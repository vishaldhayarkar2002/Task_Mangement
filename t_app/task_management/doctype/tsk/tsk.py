
import frappe
from frappe.model.document import Document

from frappe import _

def notify_user_on_assignment(doc, method):
    
    recipients = []

    if doc.assigned_to:
        recipients.append(doc.assigned_to)

    if doc.user_group:
        user_list = get_users_in_group(doc.user_group)
        recipients.extend(user_list)

    for user in set(recipients): 
        create_notification(
            user=user,
            subject="New Task Assigned",
            content=f"You have been assigned a new task: <b>{doc.title}</b>. <br> Priority: {doc.priority}, Due Date: {doc.e_date}",
            reference_doctype="tsk",
            reference_name=doc.name
        )

def notify_user_on_status_change(doc, method):
   
    if doc.has_value_changed('status'):
        recipients = []

        if doc.assigned_to:
            recipients.append(doc.assigned_to)

        if doc.user_group:
            recipients.extend(get_users_in_group(doc.user_group))

        for user in set(recipients):
            create_notification(
                user=user,
                subject="Task Status Updated",
                content=f'Task <b>"{doc.title}"</b> status has been updated to <b>{doc.status}</b>.',
                reference_doctype="tsk",
                reference_name=doc.name
            )

def notify_creator_on_completion(doc, method):
   
    if doc.has_value_changed('status') and doc.status == 'Completed':
        create_notification(
            user=doc.owner,
            subject="Task Completed",
            content=f'Task <b>"{doc.title}"</b> has been completed.',
            reference_doctype="tsk",
            reference_name=doc.name
        )

def get_users_in_group(group_name):

    return frappe.get_all(
        "User Group Member",
        filters={"parent": group_name},
        pluck="user"
    )

def create_notification(user, subject, content, reference_doctype, reference_name):

    notification_doc = frappe.get_doc({
        "doctype": "Notification Log",
        "subject": subject,
        "content": content,
        "for_user": user,
        "document_type": reference_doctype,
        "document_name": reference_name
    })
    notification_doc.insert(ignore_permissions=True)
    frappe.db.commit()

@frappe.whitelist()
def get_user_groups():
    
    user = frappe.session.user
    groups = frappe.get_all(
        "User Group Member",
        filters={"user": user},
        pluck="parent"
    )
    return groups



class tsk(Document):
    pass
