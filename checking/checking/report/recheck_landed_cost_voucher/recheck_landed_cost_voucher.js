// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt
frappe.query_reports["Recheck Landed Cost Voucher"] = {
	"filters": [
		{
			"fieldname": "landed_cost_voucher",
			"label": __("Landed Cost Voucher"),
			"fieldtype": "Link",
			"options": "Landed Cost Voucher"
		},
		{
			"fieldname": "purchase_receipt",
			"label": __("Purchase Receipt"),
			"fieldtype": "Link",
			"options": "Purchase Receipt"
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
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
			"fieldname":"group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": "no.lcv\nReceipt Document\nPurchase Receipt\nItem Code",
			"default": "Purchase Receipt"
		}
	]
}
