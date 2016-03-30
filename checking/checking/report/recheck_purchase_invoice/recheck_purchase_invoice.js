// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Purchase Invoice"] = {
	"filters": [
		{
			"fieldname": "purchase_invoice",
					"label": __("Purchase Invoice"),
					"fieldtype": "Link",
					"options": "Purchase Invoice"
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
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname": "supplier_type",
			"label": __("Supplier Type"),
			"fieldtype": "Link",
			"options": "Supplier Type",
			"default": "Service"
		}

	]
}
