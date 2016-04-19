// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Journal Entry"] = {
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
			"fieldname":"entry_document",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": " \nDraft\nSubmit"
		},
		{
			"fieldname":"recheck_month",
			"label": __("Recheck Error Input Posting Date"),
			"fieldtype": "Select",
			"options": " \nPosting Date > Created Date\nPosting Date < Created Date\nPosting Date > Document Date\nPosting Date < Document Date\nPosting Date (Year) > Document Date (Year)\nPosting Date (Year) > Created Date (Year)"
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

						if(columnDef.id == "PostingDate") {
								value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}

						if(columnDef.id == "DocumentDate") {
								value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}

						if(columnDef.id == "CreatedDate") {
								value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}

						return value;
				}
}
