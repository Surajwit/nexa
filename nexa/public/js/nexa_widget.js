frappe.provide("nexa");

nexa.Widget = class {
	constructor() {
		this.conversation = null;
		this.make_button();
	}

	make_button() {
		this.$btn = $(`<div class="nexa-fab">✨</div>`).appendTo("body");
		this.$btn.on("click", () => this.toggle_panel());
	}

	toggle_panel() {
		if (!this.$panel) this.make_panel();
		this.$panel.toggle();
	}

	make_panel() {
		this.$panel = $(`
			<div class="nexa-panel">
				<div class="nexa-header">Nexa</div>
				<div class="nexa-messages"></div>
				<div class="nexa-input-row">
					<input type="text" class="nexa-input" placeholder="Ask Nexa anything...">
				</div>
			</div>
		`).appendTo("body");

		this.$panel.find(".nexa-input").on("keydown", (e) => {
			if (e.key === "Enter") {
				this.send(e.target.value);
				e.target.value = "";
			}
		});
	}

	get_context() {
		const route = frappe.get_route();
		if (route[0] === "Form") {
			return { doctype: route[1], name: route[2] };
		}
		return {};
	}

	async send(message) {
		if (!message) return;
		if (!this.conversation) {
			const r = await frappe.call("nexa.nexa.api.start_conversation");
			this.conversation = r.message;
		}
		this.append_message("user", message);
		const r = await frappe.call("nexa.nexa.api.send_message", {
			conversation: this.conversation,
			message,
			context: this.get_context(),
		});
		this.append_message("assistant", r.message.reply);
	}

	append_message(role, content) {
		$(`<div class="nexa-msg nexa-msg-${role}">${frappe.utils.escape_html(content)}</div>`).appendTo(
			this.$panel.find(".nexa-messages")
		);
	}
};

function init_nexa() {
    if (!frappe.nexa) {
        frappe.nexa = new nexa.Widget();
    }
}

if (document.readyState === "loading") {
    $(document).on("app_ready", init_nexa);
    $(document).ready(init_nexa);
} else {
    init_nexa();
}
