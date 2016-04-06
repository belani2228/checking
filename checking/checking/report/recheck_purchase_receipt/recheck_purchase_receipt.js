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
		{
			"fieldname":"entry_type",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": " \nDraft\nTo Bill\nCompleted\nReturn",
			"default": "Draft"
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Status") {
										if(dataContext.Status == "Draft"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Status == "Completed"){
														value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}else  {
											  value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
										}
						}
						
						return value;
				}
}
