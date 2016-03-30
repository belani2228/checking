# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_delivery_note(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("No.Delivery Note")+":Link/Delivery Note:110",
		_("Posting Date") + ":Date:100",
		_("Item Code") + ":Link/Item:300",
		_("Item Name") + "::300",
		_("Item Group") + ":Link/Item Group:100",
		_("Packing (QTY)") + ":Float:100",
		_("Packing (UoM)") + "::100",
		_("Packing (Unit)") + ":Float:100",
		_("Qty") + ":Float:100",
		_("UoM") + "::50",
		_("Rate (IDR)") + ":Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Warehouse") + ":Link/Warehouse:200",
		_("Expense Account") + ":Data:200",
		_("Cost Center") + ":Link/Cost Center:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"

	]


def get_recheck_delivery_note(filters):
	conditions = get_conditions(filters)
	#return frappe.db.sql("""select item_name,item_group,stock_uom,expense_account,income_account,has_variants,is_purchase_item,is_sales_item,is_asset_item,is_sub_contracted_item from tabItem where has_variants = '0' and item_group = 'layanan' %s""" % conditions, as_list=1)
	#return frappe.db.sql("""select parent,item_code,item_name,item_group,packing_qty,packing_uom,conversion_factor,qty,stock_uom,rate,amount,warehouse,expense_account,cost_center,creation,owner,modified,modified_by from `tabDelivery Note Item` where docstatus < 2 %s""" % conditions, as_list=1)
	#return frappe.db.sql("""select `tabPurchase Receipt`.status,`tabPurchase Receipt`.name,`tabPurchase Receipt`.supplier,`tabPurchase Receipt`.company,`tabPurchase Receipt`.posting_date,`tabPurchase Receipt`.posting_time,`tabPurchase Receipt`.transporter_name,`tabPurchase Receipt`.lr_date,`tabPurchase Receipt`.lr_no,`tabPurchase Receipt`.currency,`tabPurchase Receipt`.price_list_currency,`tabPurchase Receipt`.conversion_rate,`tabPurchase Receipt`.base_net_total,concat(`tabCurrency`.symbol," ",`tabPurchase Receipt`.base_grand_total),`tabPurchase Receipt`.net_total,`tabPurchase Receipt`.base_total,`tabPurchase Receipt`.base_rounded_total from `tabPurchase Receipt` inner join `tabCurrency` on `tabPurchase Receipt`.currency = `tabCurrency`.name where `tabPurchase Receipt`.docstatus < 2 %s""" % conditions, as_list=1)
	return frappe.db.sql(
		"""select
				dn1.status,dn2.parent,dn1.posting_date,dn2.item_code,dn2.item_name,dn2.item_group,dn2.packing_qty,dn2.packing_uom,dn2.conversion_factor,
		        dn2.qty,dn2.stock_uom,dn2.rate,dn2.amount,dn2.warehouse,dn2.expense_account,dn2.cost_center,dn2.creation,
				dn2.owner,dn2.modified,dn2.modified_by
		   from
		   		`tabDelivery Note Item` dn2 inner join `tabDelivery Note` dn1

		   where
		   		dn2.parent = dn1.name and dn2.docstatus < 2 %s order by dn1.posting_date desc,dn1.posting_time desc,dn2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("delivery_note"):
		conditions += "and dn2.parent = '%s'" % filters["delivery_note"]

	if filters.get("item_group"):
		conditions += "and dn2.item_group = '%s'" % filters["item_group"]

	if filters.get("warehouse"):
		conditions += "and dn2.warehouse = '%s'" % filters["warehouse"]

	if filters.get("from_date"):
		conditions += "and dn1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and dn1.posting_date <= '%s'" % filters["to_date"]

	if filters.get("cost_center"):
		conditions += "and dn2.cost_center = '%s'" % filters["cost_center"]

	return conditions

		#if filters.get("company"): conditions += " and company = '%s'" % \
		#	filters["company"].replace("'", "\\'")
