import frappe

from nexa.nexa.tools import action_tools, data_tools
from nexa.nexa.tools.registry import TOOLS

TOOL_HANDLERS = {
	"get_document": data_tools.get_document,
	"list_documents": data_tools.list_documents,
	"create_document": action_tools.create_document,
}

NEEDS_CONFIRMATION = {"create_document"}


def run_tool(tool_name: str, tool_input: dict):
	handler = TOOL_HANDLERS.get(tool_name)
	if not handler:
		frappe.throw(f"Unknown tool: {tool_name}")
	return handler(**tool_input)


def get_settings():
	settings = frappe.get_single("Nexa Settings")
	if not settings.enabled:
		frappe.throw("Nexa is disabled")
	return settings
