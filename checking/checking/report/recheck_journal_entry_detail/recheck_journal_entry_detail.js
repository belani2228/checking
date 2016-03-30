// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Journal Entry Detail"] = {
	"filters": [
		{
			"fieldname": "journal_entry",
			"label": __("Journal Entry"),
			"fieldtype": "Link",
			"options": "Journal Entry"
		},
		{
			"fieldname":"entry_type",
			"label": __("Document Type"),
			"fieldtype": "Select",
			"options": " \nJournal Entry\nCash Entry\nBank Entry\nDebit Note\nCredit Note\nWrite Off Entry",
			"default": "Cash Entry"
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
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"get_query": function() {
				return {
					"query": "erpnext.controllers.queries.get_account_list",
					"filters": [
						['Account', 'is_group', '=', 0],
						['Account', 'freeze_account', '=', 'No'],
					]
				}
			}
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center"
		},

	]
}
