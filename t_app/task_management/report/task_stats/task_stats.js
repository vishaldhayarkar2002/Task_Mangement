// Copyright (c) 2025, vishal and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Task Stats"] = {
    "filters": [
        {
            "fieldname": "assigned_to",
            "label": __("Assigned To"),
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": [
                __("Open"),
                __("In Progress"),
                __("Completed")
            ]
        }
    ]
};
