// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Delivery Note"] = {
	"filters": [
		{
			"fieldname": "delivery_note",
					"label": __("Delivery Note"),
					"fieldtype": "Link",
					"options": "Delivery Note"
		},
		{
			"fieldname": "customer_group",
					"label": __("Customer Group"),
					"fieldtype": "Link",
					"options": "Customer Group"
		},
		{
			"fieldname": "territory",
					"label": __("Territory"),
					"fieldtype": "Link",
					"options": "Territory"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_end()
		}
	]
}
