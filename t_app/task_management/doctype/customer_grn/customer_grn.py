import frappe
from frappe.model.document import Document

class CustomerGRN(Document):

    def before_submit(self):
        self.check_exceed_qty()
        self.update_sales_invoice_status()

    def on_trash(self):

        self.revert()

    @frappe.whitelist()
    def get_sales_invoices(self):
        sales_items = frappe.get_all(
            "Sales Invoice Item", 
            filters={"parent": self.sales_invoice, "custom_customer_grn": 0},  
            fields=["item_code", "item_name", "qty", "uom", "name"]
        )

        for item in sales_items:
            received_qty = frappe.db.get_value(
                "Customer GRN Items", 
                {"item_reference": item.name}, 
                "sum(qty)"
            ) or 0

            self.append("customer_grn_items", {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": 0,
                "uom": item.uom,
                "item_reference": item.name,
                "remaining_qty": item.qty - received_qty
            })

    @frappe.whitelist()
    def check_exceed_qty(self):
        for item in self.customer_grn_items:
            si_item_qty = frappe.db.get_value("Sales Invoice Item", item.item_reference, "qty")
            received_qty = frappe.db.get_value(
                "Customer GRN Items",
                {"item_reference": item.item_reference, "parent": ["!=", self.name]},
                "sum(qty)"
            ) or 0

            item.remaining_qty = si_item_qty - received_qty

            if item.qty + received_qty > si_item_qty:
                frappe.throw(f"Quantity exceeds Sales Invoice limit")

    def update_sales_invoice_status(self):
        for item in self.customer_grn_items:
            si_item_qty = frappe.db.get_value("Sales Invoice Item", item.item_reference, "qty")
            received_qty = frappe.db.get_value(
                "Customer GRN Items",
                {"item_reference": item.item_reference},
                "sum(qty)"
            ) or 0
            remaining_qty = si_item_qty - received_qty

            frappe.msgprint("Remaining Qty: " + str(remaining_qty))

            
            frappe.db.set_value("Sales Invoice Item", item.item_reference, "custom_customer_grn", int(remaining_qty == 0))

        any_pending = frappe.db.get_value(
            "Sales Invoice Item", 
            {"parent": self.sales_invoice, "custom_customer_grn": 0}, 
            "name"
        )
        
        if not any_pending:
            frappe.db.set_value("Sales Invoice", self.sales_invoice, "custom_customer_grn_status", 1)

    def revert(self):
       
        for item in self.customer_grn_items:
            received_qty = frappe.db.get_value(
                "Customer GRN Items",
                {"item_reference": item.item_reference, "parent": ["!=", self.name]},
                "sum(qty)"
            ) or 0

            si_item_qty = frappe.db.get_value("Sales Invoice Item", item.item_reference, "qty")
            remaining_qty = si_item_qty - received_qty

            frappe.db.set_value("Sales Invoice Item", item.item_reference, "custom_customer_grn", int(remaining_qty == 0))

        any_completed = frappe.db.get_value(
            "Sales Invoice Item",
            {"parent": self.sales_invoice, "custom_customer_grn": 1},
            "name"
        )

       
        if not any_completed:
            frappe.db.set_value("Sales Invoice", self.sales_invoice, "custom_customer_grn_status", 0)
