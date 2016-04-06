// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Purchase Invoice LCV Item"] = {
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
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center"
		},
		{
			"fieldname":"entry_type",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": " \nDraft\nOverdue\nPaid",
			"default": "Draft"
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
										if(dataContext.SupplierType == "Import"){
												value = "<span style='color:#8B4513;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.SupplierType == "Service"){
														value = "<span style='color:#000080;font-weight:bold'>" + value + "</span>";
										}else  {
											  value = "<span style='color:#006400;font-weight:bold'>" + value + "</span>";
										}
						}

						return value;
				}
}
