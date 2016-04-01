// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["List Item Product"] = {
	"filters": [
		{
			"fieldname":"entry_type",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Disabled\nEnabled",
			"default": "Disabled"
		}
	]
}
