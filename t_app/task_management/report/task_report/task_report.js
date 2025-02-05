// Copyright (c) 2025, vishal and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Task Report"] = {
    "filters": [
        {
            "fieldname": "assigned_to",
            "label": __("Assigned To"),
            "fieldtype": "Link",
            "options": "User"
        }
    ]
};