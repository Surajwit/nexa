import frappe


def create_document(doctype: str, values: dict):
	if not frappe.has_permission(doctype, "create"):
		frappe.throw("Not permitted", frappe.PermissionError)
	doc = frappe.get_doc({"doctype": doctype, **values})
	doc.insert()
	return doc.as_dict()
