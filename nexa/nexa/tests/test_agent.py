import frappe
from frappe.tests.utils import FrappeTestCase


class TestNexaAgent(FrappeTestCase):
	def test_settings_disabled_blocks(self):
		frappe.db.set_single_value("Nexa Settings", "enabled", 0)
		from nexa.nexa.agent import get_settings

		with self.assertRaises(frappe.ValidationError):
			get_settings()
