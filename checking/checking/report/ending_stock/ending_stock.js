// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Ending Stock"] = {
	"filters": [
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item"
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Warehouse"
		},
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Qty") {
									  if(dataContext.Qty == "0"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else{
											if(dataContext.Qty <0){
											    value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
											}
										}
						}

						if (columnDef.id == "PackingQty") {
									  if(dataContext.PackingQty == "0"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else{
											if(dataContext.PackingQty <0){
											    value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
											}
										}
						}

						if (columnDef.id == "StockUOM") {
										if(dataContext.StockUOM == "Kg"){
											if(dataContext.PackingUoM != "Karung"){
												value = "<span style='color:brown;font-weight:bold'>" + value + "</span>";
											}
										}else{
											if(dataContext.StockUOM!= "Ctn"){
												if(dataContext.PackingUoM != "Ctn"){
													value = "<span style='color:brown;font-weight:bold'>" + value + "</span>";
												}
											}
										}
						}

						if (columnDef.id == "PackingUoM") {
										if(dataContext.StockUOM == "Kg"){
											if(dataContext.PackingUoM != "Karung"){
												value = "<span style='color:brown;font-weight:bold'>" + value + "</span>";
											}
										}else{
											if(dataContext.StockUOM!= "Ctn"){
												if(dataContext.PackingUoM != "Ctn"){
													value = "<span style='color:brown;font-weight:bold'>" + value + "</span>";
												}
											}
										}
						}




						return value;
				}
}
