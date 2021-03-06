// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Purchase Invoice LCV"] = {
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
			"options": " \nPosting Date > Created Date\nPosting Date < Created Date\nPosting Date > Document Date\nPosting Date < Document Date\nPosting Date (Year) > Document Date (Year)\nPosting Date (Year) > Created Date (Year)"
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

						if (columnDef.id == "SupplierType") {
									if(dataContext.SupplierType == "Service"){
														value = "<span style='color:#000080;font-weight:bold'>" + value + "</span>";
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
