// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Delivery Note Item"] = {
	"filters": [
		{
			"fieldname": "delivery_note",
			"label": __("Delivery Note"),
			"fieldtype": "Link",
			"options": "Delivery Note"
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
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
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
			"options": " \nDraft\nTo Bill\nCompleted\nReturn",
			"default": "Draft"
		},
		{
			"fieldname":"recheck_warehouse",
			"label": __("recheck warehouse if input wrong cost center"),
			"fieldtype": "Select",
			"options": " \nGudang Buah-Dadap\nGudang Bawang-Dadap\nGudang Suri\nGudang Pios\nToko Pios\nToko Puspa\nToko Songoyudan",
		},
		{
			"fieldname":"recheck_customer",
			"label": __("recheck customer use wrong warehouse"),
			"fieldtype": "Select",
			"options": " \nCustomer Buah-Jkt\nCustomer Bawang-Jkt\nCustomer AKS-Sby"
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
						
						if (columnDef.id == "Document") {
										if(dataContext.Document == "Return"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}
						}

						return value;
				}
}
