# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, fmt_money
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_list_item_product(filters)

	return columns, data

def get_columns():
	return [
		_("Item Code")+":Link/Item:100",
		_("Item Name") + ":Data:100",
		_("Warehouse") + ":Data:100",
		_("Stock UOM") + ":Data:100",
		_("Qty") + ":Float:100",
		_("Packing UoM") + ":Data:100",
		_("Packing Qty") + ":Float:100"
	]

def get_list_item_product(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
	select
     	sle.`item_code`,
     	it.`item_name`,
     	sle.`warehouse`,
     	sle.`stock_uom`,
     	sum(IF(sle.voucher_type = 'Stock Reconciliation',sle.qty_after_transaction,sle.actual_qty)) as bola,
     	IF(sle.`voucher_type` = 'Delivery Note', (select `packing_uom` from `tabDelivery Note Item` WHERE `name` = sle.`voucher_detail_no`), IF(sle.`voucher_type` = 'Purchase Receipt', (select `uom` FROM `tabPurchase Receipt Item` WHERE `name` = sle.`voucher_detail_no`), IF(sle.`voucher_type` = 'Stock Entry', (select `packing_uom` FROM `tabStock Entry Detail` WHERE `name` = sle.`voucher_detail_no`), (select `packing_uom` FROM `tabStock Reconciliation Item` WHERE `parent` = sle.`voucher_no` AND `item_code` = sle.`item_code`)))) AS packinguom,
     	sum(IF(sle.`voucher_type` = 'Delivery Note', (select `packing_qty`*-1 from `tabDelivery Note Item` WHERE `name` = sle.`voucher_detail_no`), IF(sle.`voucher_type` = 'Purchase Receipt', (select `received_qty` from `tabPurchase Receipt Item` where `name` = sle.`voucher_detail_no`), IF(sle.`voucher_type` = 'Stock Entry', (select IF(sle.`actual_qty` <= 1, `packing_qty`*-1, `packing_qty`) FROM `tabStock Entry Detail` WHERE `name` = sle.`voucher_detail_no`), (select `packing_qty` FROM `tabStock Reconciliation Item` WHERE `parent` = sle.`voucher_no` AND `item_code` = sle.`item_code`))))) AS packingqty

    FROM
     	`tabStock Ledger Entry` sle, `tabItem` it
    WHERE
     	sle.`item_code` = it.`name` AND
     	sle.`docstatus` = '1' %s
	GROUP BY
		sle.item_code,sle.warehouse
	""" %conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("to_date"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and sle.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])

	if filters.get("item_code"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and sle.item_code = '%s'" % frappe.db.escape(filters["item_code"])

	if filters.get("warehouse"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and sle.warehouse = '%s'" % frappe.db.escape(filters["warehouse"])

	return conditions
