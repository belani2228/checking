// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Check Error Delivery Note Item"] = {
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
			"label": __("Recheck DN-SI"),
			"fieldtype": "Select",
			"options": "Posting Date DN-SI\nCustomer DN-SI\nCost Center DN-SI\nWarehouse DN-SI\nItem DN-SI",
			"default": "Posting Date DN-SI"
		}
	]
	}
