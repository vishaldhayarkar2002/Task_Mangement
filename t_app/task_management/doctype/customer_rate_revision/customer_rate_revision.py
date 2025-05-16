import frappe
from frappe.model.document import Document

class CustomerRateRevision(Document):
	def before_submit(self):
		self.update_customer_rate_details()

	@frappe.whitelist()
	def update_customer_rate_details(self):
		if not self.item_code:
			return

		rate_sum = 0
		amount_sum = 0

		customer_rate_details_docs = frappe.get_all("Customer Rate Details", {"item_code": self.item_code, "customer" : self.customer , "company" : self.company},
		["name","rate"])

		# frappe.throw(str(customer_rate_details_docs))
		for customer_rate in customer_rate_details_docs:
			# First loop with filter
			child_items = frappe.get_all("Customer Rate Bifurcation", {"parent": customer_rate.name,"item_code":self.item_code},["name","item_code","rate","qty","amount"])
			for i in child_items:
				frappe.db.set_value(
					"Customer Rate Bifurcation", 
					i.name, 
					{
						"rate": self.rate,
						"amount": self.rate * i.qty
					}
				)

			# # Second loop without any filter
			rate_sum,amount_sum = frappe.get_value("Customer Rate Bifurcation", {"parent": customer_rate.name},["sum(rate) as rate_sum","sum(amount) as amount_sum"])
			# for i in all_child_items:
			# 	# rate_sum += i.rate
			# 	# amount_sum += i.amount
			# rate_sum = self.calculate_total(child_table="items",total_field="rate",condition_field= "rate")
			if rate_sum and amount_sum:
				frappe.db.set_value(
					"Customer Rate Details",
					customer_rate.name,
					{
						"rate": rate_sum,
						"total_amount": amount_sum,
						"valid_from": self.valid_from,
						"valid_to": self.valid_to
					}
				)

			# Create a new document
			new_doc = frappe.new_doc('Item Price')
			new_doc.item_code = self.item_code
			new_doc.price_list = self.price_list
			new_doc.price_list_rate = rate_sum
			new_doc.currency = self.currency
			new_doc.valid_from = self.valid_from
			new_doc.valid_upto = self.valid_to
			new_doc.customer = self.customer
			new_doc.company = self.company
			new_doc.item_name = self.item_name
			new_doc.uom = self.uom
			new_doc.currency = self.currency
			new_doc.custom_customer_rate_details = customer_rate.name

			new_doc.insert()