// Copyright (c) 2016, molie and contributors
// For license information, please see license.txt

frappe.query_reports["Recheck Stock Entry Detail"] = {
	"filters": [
		{
			"fieldname": "stock_entry",
			"label": __("Stock Entry"),
			"fieldtype": "Link",
			"width": "150",
			"options": "Stock Entry"
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
			"fieldname":"purpose",
			"label": __("Document"),
			"fieldtype": "Select",
			"options": " \nMaterial Issue\nMaterial Receipt\nMaterial Transfer\nRepack\nMaterial Transfer for Manufacture\nManufacture\nSubcontract",
			"default": ""
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
			"options": " \nDraft\nSubmitted",
			"default": "Draft"
		},
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
						value = default_formatter(row, cell, value, columnDef, dataContext);
						if (columnDef.id == "Status") {
										if(dataContext.Status == "Draft"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else  {
												value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}
						}

						if (columnDef.id == "Document") {
										if(dataContext.Document == "Material Issue"){
												value = "<span style='color:orange;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Document == "Material Receipt"){
												value = "<span style='color:blue;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Document == "Material Transfer"){
												value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Document == "Repack"){
												value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Document == "Subcontract"){
												value = "<span style='color:brown;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.Document == "Manufacture"){
												value = "<span style='color:black;font-weight:bold'>" + value + "</span>";
										}else  {
													value = "<span style='color:pink;font-weight:bold'>" + value + "</span>";
										}
						}

						if(columnDef.id == "PostingDate") {
										value = "<span style='color:#AA6E39;font-weight:bold'>" + value + "</span>";
						}


						if (columnDef.id == "TotalAmount") {
									  if(dataContext.TotalAmount <0){
												  value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.TotalAmount >0){
														value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}
						}

						if (columnDef.id == "ValuationRate") {
										if(dataContext.ValuationRate < dataContext.BasicRate){
													value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.ValuationRate > dataContext.BasicRate){
														value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}
						}

						if (columnDef.id == "BasicRate") {
										if(dataContext.ValuationRate < dataContext.BasicRate){
													value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}else if(dataContext.ValuationRate > dataContext.BasicRate){
														value = "<span style='color:red;font-weight:bold'>" + value + "</span>";
										}
						}

						if (columnDef.id == "AdditionalCost") {
										if(dataContext.AdditionalCost >0){
													value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
										}
						}




						return value;
		}
	}
