# Nexa

**Nexa** is an AI-powered chatbot for ERPNext that lives on every Desk page. It understands what record or page you're viewing, can answer questions about your data, and can take actions (with confirmation) — all scoped to the logged-in user's permissions.

## Features

- 💬 **Always available** — a floating chat widget loaded globally across every Desk page
- 🧠 **Context-aware** — knows which doctype/record you're currently viewing
- 🔒 **Permission-safe** — every data read or write runs through Frappe's own permission checks for the logged-in user, never an admin/service account
- 🛠️ **Tool-calling** — the LLM can fetch documents, list/search records, and (with confirmation) create documents
- ⚙️ **Configurable** — pick your LLM provider, model, and system prompt from a single settings page

## Installation

\`\`\`bash
bench get-app nexa https://github.com/<your-username>/nexa
bench --site [sitename] install-app nexa
bench --site [sitename] migrate
bench build --app nexa
\`\`\`

## Setup

1. Open **Nexa Settings** (single doctype) in the Desk
2. Choose a **Provider** (OpenAI / Anthropic) and **Model**
3. Add your **API Key**
4. Enable it

Once enabled, a floating button appears in the bottom-right corner of every Desk page.

## Project structure

\`\`\`
nexa/
├── hooks.py                  # app_include_js / app_include_css registration
├── nexa/
│   ├── agent.py                # tool dispatch + settings validation
│   ├── api.py                   # whitelisted endpoints called by the widget
│   ├── doctype/
│   │   ├── nexa_conversation/    # one per chat session
│   │   ├── nexa_message/          # individual messages in a conversation
│   │   └── nexa_settings/         # provider/model/API key config (single)
│   └── tools/
│       ├── registry.py           # tool schemas exposed to the LLM
│       ├── data_tools.py          # read-only: get_document, list_documents
│       └── action_tools.py        # write actions: create_document
└── public/
    ├── js/                     # floating widget (nexa.bundle.js, nexa_widget.js)
    └── css/                    # widget styling (nexa.css)
\`\`\`

## What's implemented vs. what's left

**Done:** doctypes for conversations/messages/settings, permission-checked data tools, whitelisted API layer, and the floating chat widget.

**Still to do:**
- Wire an actual LLM API call into `nexa/nexa/api.py::send_message` (currently a placeholder)
- Add streaming responses via `frappe.publish_realtime`
- Add a confirmation UI in the widget for write-actions like `create_document`

## Security notes

Every tool call runs through `frappe.has_permission()` using the current session user — the chatbot can never see or modify data the logged-in user couldn't already access directly. Destructive actions (create, update, submit) are gated behind explicit user confirmation before execution.

## License

MIT
