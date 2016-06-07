# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_list_item_product(filters)

	return columns, data

def get_columns():
	return [
		_("Item Code")+":Link/Item:300",
		_("Item Name") + ":Data:300",
		_("Item Group") + ":Data:100",
		_("UoM") + ":Data:50"

	]

def get_list_item_product(filters):
	conditions = get_conditions(filters)

	return frappe.db.sql("""
		select
			item_code,
			item_name,
			item_group,
			stock_uom
		from
			`tabItem`
		where
			has_variants = '0'
			and item_group != 'bahan baku'
			and item_group != 'layanan'
			and item_name != 'dummy'
			and item_code not in (select distinct item_code from `tabDelivery Note Item`)
			%s""" %conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("entry_type") == "Disabled":
		conditions += "and disabled = '1'"
	else:
		conditions += "and disabled = '0'"
	return conditions
