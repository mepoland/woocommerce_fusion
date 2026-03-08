import frappe


def execute():
	"""
	Add a default Order Header Field mapping (po_no ← $.number) to every existing
	WooCommerce Server that has no order_field_map rows yet.

	This preserves the exact backward-compatible behaviour for users upgrading from
	versions that hardcoded `po_no = wc_order.id`.

	Servers that already have rows in order_field_map are left untouched so that
	intentional configurations are never overwritten.
	"""
	frappe.reload_doc("woocommerce", "doctype", "woocommerce_server_order_field")
	frappe.reload_doc("woocommerce", "doctype", "woocommerce_server")

	for name in frappe.get_all("WooCommerce Server", pluck="name"):
		doc = frappe.get_doc("WooCommerce Server", name)
		if doc.order_field_map:
			continue

		doc.append(
			"order_field_map",
			{
				"erpnext_field_name": "po_no | Customer's Purchase Order Number",
				"woocommerce_field_name": "$.id",
			},
		)
		doc.save()
		print(f"Added default order_field_map to WooCommerce Server: {name}")
