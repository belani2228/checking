# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_list_item_service(filters)

	return columns, data

def get_columns():
	return [

		_("Item Code / Name") + ":Data:150",
		_("Item Group") + ":Data:80",
		_("UoM") + ":Data:50",
		_("Expense Account") + ":Data:300",
		_("Income Account") + ":Data:100",
		_("Has Variants") + ":Data:80",
		_("Is Purchase Item") + ":Data:80",
		_("Is Sales Item") + ":Data:80",
		_("Is Asset Item") + ":Data:80",
		_("Is Fixed Item") + ":Data:80",
		_("Is Sub Contracted Item") + ":Data:80"
	]

def get_list_item_service(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select
			item_name,
			item_group,
			stock_uom,
			expense_account,
			income_account,
			if(has_variants = '1',"Yes","No") as hasvariants,
			if(is_purchase_item = '1',"Yes","No") as ispurchaseitem,
			if(is_sales_item = '1',"Yes","No") as issalesitem,
			if(is_asset_item = '1',"Yes","No") as issassetitem,
			if(is_fixed_asset = '1',"Yes","No") as isfixeditem,
			if(is_sub_contracted_item = '1',"Yes","No") as issubcontracteditem
		from
			`tabItem`
		where
			has_variants = '0'
			and item_group = 'layanan' %s
		order by
			item_code asc,item_name asc
			""" %conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("entry_type") == "Disabled":
		conditions += "and disabled = '1'"
	else:
		conditions += "and disabled = '0'"
	return conditions
