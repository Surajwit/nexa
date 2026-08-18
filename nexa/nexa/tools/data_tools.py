import frappe


def get_document(doctype: str, name: str):
	if not frappe.has_permission(doctype, "read", doc=name):
		frappe.throw("Not permitted", frappe.PermissionError)
	doc = frappe.get_doc(doctype, name)
	return doc.as_dict()


def list_documents(doctype: str, filters=None, fields=None, limit: int = 20):
	if not frappe.has_permission(doctype, "read"):
		frappe.throw("Not permitted", frappe.PermissionError)
	return frappe.get_list(
		doctype,
		filters=filters or {},
		fields=fields or ["name"],
		limit_page_length=min(limit, 100),
	)
