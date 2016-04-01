// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Check Error Landed Cost Voucher"] = {
	"filters": [
		{
			"fieldname": "landed_cost_voucher",
			"label": __("Landed Cost Voucher"),
			"fieldtype": "Link",
			"options": "Landed Cost Voucher"
		},
		{
			"fieldname":"from_date",
			"label": __("From Modified Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Modified Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_end()
		}
	]
}
