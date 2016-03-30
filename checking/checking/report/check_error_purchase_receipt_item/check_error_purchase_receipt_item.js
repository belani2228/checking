// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Check Error Purchase Receipt Item"] = {
		"filters": [
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
				"fieldname":"recheck_group",
				"label": __("Recheck PR-PI"),
				"fieldtype": "Select",
				"options": "Posting Date PR-PI\nSupplier PR-PI\nCost Center PR-PI\nItem PR-PI",
				"default": "Posting Date PR-PI"
			}
		]
		}
