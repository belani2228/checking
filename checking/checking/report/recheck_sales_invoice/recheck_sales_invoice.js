// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Sales Invoice"] = {
	"filters": [
		{
			"fieldname": "sales_invoice",
					"label": __("Sales Invoice"),
					"fieldtype": "Link",
					"options": "Sales Invoice"
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
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "customer_group",
			"label": __("Customer Group"),
			"fieldtype": "Link",
			"options": "Customer Group",
			"default": "Bawang-Dadap"
		},
		{
			"fieldname": "territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory"
		},
		{
			"fieldname":"entry_type",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": " \nDraft\nOverdue\nPaid",
			"default": "Draft"
		},
		{
			"fieldname":"recheck_month",
			"label": __("Recheck Error Input Posting Date"),
			"fieldtype": "Select",
			"options": " \nIf Posting Date > Created Date\nIf Posting Date < Created Date\nError Input Year"
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Status") {
										if(dataContext.Status == "Draft"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Status == "Paid"){
														value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}else  {
											  value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
										}
						}

						if(columnDef.id == "PostingDate") {
										value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}

						if(columnDef.id == "CreatedDate") {
										value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}

						return value;
				}
}
