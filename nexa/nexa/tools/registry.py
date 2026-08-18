"""Tool schemas exposed to the LLM. Every handler must run permission-checked."""

TOOLS = [
	{
		"name": "get_document",
		"description": "Fetch a single document by doctype and name, respecting user permissions.",
		"input_schema": {
			"type": "object",
			"properties": {
				"doctype": {"type": "string"},
				"name": {"type": "string"},
			},
			"required": ["doctype", "name"],
		},
	},
	{
		"name": "list_documents",
		"description": "List/search documents of a doctype with filters, respecting user permissions.",
		"input_schema": {
			"type": "object",
			"properties": {
				"doctype": {"type": "string"},
				"filters": {"type": "object"},
				"fields": {"type": "array", "items": {"type": "string"}},
				"limit": {"type": "integer", "default": 20},
			},
			"required": ["doctype"],
		},
	},
	{
		"name": "create_document",
		"description": "Create a new document. Requires user confirmation before execution.",
		"input_schema": {
			"type": "object",
			"properties": {
				"doctype": {"type": "string"},
				"values": {"type": "object"},
			},
			"required": ["doctype", "values"],
		},
	},
]
