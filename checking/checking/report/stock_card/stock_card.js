// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Card"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher #"),
			"fieldtype": "Data"
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Qty") {
										if(dataContext.VoucherType == "Stock Entry"){
											if(dataContext.Qty >0){
												value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
											}else{
												if(dataContext.Qty == 0){
											   	value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
												}
											}
										}else{
											if(dataContext.VoucherType == "Purchase Receipt"){
											    value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
											}
										}
						}

						if (columnDef.id == "PackingQty") {
										if(dataContext.VoucherType == "Stock Entry"){
											if(dataContext.PackingQty >0){
												value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
											}else{
												if(dataContext.PackingQty == 0){
											   	value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
												}
											}
										}else{
											if(dataContext.VoucherType == "Purchase Receipt"){
											    value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
											}
										}
						}

						if (columnDef.id == "VoucherType") {
									  if(dataContext.VoucherType == "Stock Entry"){
											if(dataContext.Qty >1){
												value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
											}
										}else{
											if(dataContext.VoucherType == "Purchase Receipt"){
											    value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
											}
										}
						}


						return value;
				}
}
