// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Purchase Receipt"] = {
	"filters": [
		{
			"fieldname": "purchase_receipt",
					"label": __("Purchase Receipt"),
					"fieldtype": "Link",
					"options": "Purchase Receipt"
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
		},
	]
}
