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
		{
			"fieldname":"entry_document",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": " \nDraft\nSubmit"
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Status") {
										if(dataContext.Status == "Draft"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Status == "Submit"){
														value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}
						}

						if (columnDef.id == "VoucherType") {
										if(dataContext.VoucherType == "Cash Entry"){
												value = "<span style='color:#8B4513;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.VoucherType == "Bank Entry"){
														value = "<span style='color:#000080;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.VoucherType == "Journal Entry"){
											  value = "<span style='color:#006400;font-weight:bold'>" + value + "</span>";
										}else  {
											  value = "<span style='color:#000000;font-weight:bold'>" + value + "</span>";
										}
						}

						return value;
				}
}
