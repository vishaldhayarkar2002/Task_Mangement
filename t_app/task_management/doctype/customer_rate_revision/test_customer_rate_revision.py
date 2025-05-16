import frappe

# def after_save(doc, method):
#     """Trigger when a new Customer Rate Revision is saved."""

#     # Fetch the updated rate details from the new document
#     for rate_detail in doc.customer_rate_details:
#         customer_rate_type = rate_detail.customer_rate_type
#         item_code = rate_detail.item_code
#         new_rate = rate_detail.rate

#         # Find all relevant Customer Rate Details documents
#         customer_rate_docs = frappe.get_all("Customer Rate Details",
#                                             filters={"customer_rate_type": customer_rate_type},
#                                             fields=["name"])

#         for rate_doc in customer_rate_docs:
#             # Load the full document
#             customer_rate_doc = frappe.get_doc("Customer Rate Details", rate_doc.name)

#             # Update the rate in Customer Rate Bifurcation table
#             updated = False
#             for bifurcation in customer_rate_doc.customer_rate_bifurcation:
#                 if bifurcation.customer_rate_type == customer_rate_type and bifurcation.item_code == item_code:
#                     bifurcation.rate = new_rate
#                     updated = True
            
#             # Save the document after updating if changes were made
#             if updated:
#                 customer_rate_doc.save()
#                 frappe.db.commit()  # Commit changes to the database

#     frappe.msgprint("Customer rate details updated successfully.")
