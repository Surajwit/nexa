import frappe

from nexa.nexa.agent import NEEDS_CONFIRMATION, get_settings, run_tool


@frappe.whitelist()
def start_conversation(title: str = None):
	conv = frappe.get_doc(
		{"doctype": "Nexa Conversation", "user": frappe.session.user, "title": title or "New chat"}
	)
	conv.insert()
	return conv.name


@frappe.whitelist()
def send_message(conversation: str, message: str, context: dict = None):
	conv = frappe.get_doc("Nexa Conversation", conversation)
	if conv.user != frappe.session.user:
		frappe.throw("Not permitted", frappe.PermissionError)

	get_settings()  # validates enabled + config

	frappe.get_doc(
		{
			"doctype": "Nexa Message",
			"conversation": conversation,
			"role": "user",
			"content": message,
			"reference_doctype": (context or {}).get("doctype"),
			"reference_name": (context or {}).get("name"),
		}
	).insert()

	# TODO: call your LLM provider here with conversation history + TOOLS,
	# loop on tool_use responses via run_tool(), stream partials via
	# frappe.publish_realtime(f"nexa:{conversation}", {...})
	reply = "Wire up your LLM provider call here."

	frappe.get_doc(
		{"doctype": "Nexa Message", "conversation": conversation, "role": "assistant", "content": reply}
	).insert()

	return {"reply": reply}


@frappe.whitelist()
def confirm_tool_call(conversation: str, tool_name: str, tool_input: dict, approved: bool):
	if not approved:
		return {"status": "cancelled"}
	if tool_name not in NEEDS_CONFIRMATION:
		frappe.throw("Tool does not require confirmation")
	result = run_tool(tool_name, tool_input)
	return {"status": "executed", "result": result}


@frappe.whitelist()
def get_messages(conversation: str):
	conv = frappe.get_doc("Nexa Conversation", conversation)
	if conv.user != frappe.session.user:
		frappe.throw("Not permitted", frappe.PermissionError)
	return frappe.get_list(
		"Nexa Message",
		filters={"conversation": conversation},
		fields=["role", "content", "timestamp"],
		order_by="timestamp asc",
	)
