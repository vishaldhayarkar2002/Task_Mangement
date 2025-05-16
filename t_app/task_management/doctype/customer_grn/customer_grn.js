// Copyright (c) 2025, vishal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer GRN", 
    {

    setup:function(frm) {
        frm.set_query("sales_invoice", function() {
            return {
            filters: [
            ["Sales Invoice", "customer", '=', frm.doc.customer],
			["Sales Invoice", "company", '=', frm.doc.company],
            ["Sales Invoice", "docstatus", '=', 1],
            ["Sales Invoice", "custom_customer_grn_status", '=', 0]
            ]
        };
        });
    },

    sales_invoice: async function(frm) {
        frm.clear_table("customer_grn_items");
        frm.refresh_field("customer_grn_items");

        await frm.call({
            method: "get_sales_invoices",
            doc: frm.doc,
        });

        frm.refresh_field("customer_grn_items");
    },
});
