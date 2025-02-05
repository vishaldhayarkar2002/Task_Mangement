# Copyright (c) 2025, Vishal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# t_app/task_management/doctype/tsk/tsk.py

from frappe import _

def notify_user_on_assignment(doc, method):
    """
    Create system notifications for the assigned user or all users in an assigned group.
    """
    recipients = []

    # If task is assigned to a specific user
    if doc.assigned_to:
        recipients.append(doc.assigned_to)

    # If task is assigned to a user group, get all users from that group
    if doc.user_group:
        user_list = get_users_in_group(doc.user_group)
        recipients.extend(user_list)

    # Send notifications to all recipients
    for user in set(recipients):  # Avoid duplicate notifications
        create_notification(
            user=user,
            subject="New Task Assigned",
            content=f"You have been assigned a new task: <b>{doc.title}</b>. <br> Priority: {doc.priority}, Due Date: {doc.e_date}",
            reference_doctype="tsk",
            reference_name=doc.name
        )

def notify_user_on_status_change(doc, method):
    """
    Create system notifications when the task status is updated.
    """
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
    """
    Notify the task creator when the task is marked as completed.
    """
    if doc.has_value_changed('status') and doc.status == 'Completed':
        create_notification(
            user=doc.owner,
            subject="Task Completed",
            content=f'Task <b>"{doc.title}"</b> has been completed.',
            reference_doctype="tsk",
            reference_name=doc.name
        )

def get_users_in_group(group_name):
    """
    Fetch all users assigned to a given user group.
    """
    return frappe.get_all(
        "User Group Member",
        filters={"parent": group_name},
        pluck="user"
    )

def create_notification(user, subject, content, reference_doctype, reference_name):
    """
    Helper function to create a system notification.
    """
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
    """
    Returns the list of user groups the logged-in user belongs to.
    """
    user = frappe.session.user
    groups = frappe.get_all(
        "User Group Member",
        filters={"user": user},
        pluck="parent"
    )
    return groups



class tsk(Document):
    pass
