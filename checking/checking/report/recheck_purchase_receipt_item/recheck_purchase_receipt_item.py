# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_purhase_receipt(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("No.Puchase Receipt")+":Link/Purchase Receipt:120",
		_("Posting Date") + ":Date:100",
		_("Supplier Name") + ":Link/Supplier:200",
		_("Item Code") + ":Link/Item:300",
		_("Item Name") + "::300",
		_("Item Group") + ":Link/Item Group:100",
		_("Qty") + ":Float:100",
		_("UoM") + "::50",
		_("Received (QTY)") + ":Float:100",
		_("Packing (QTY)") + ":Float:100",
		_("Packing (UoM)") + "::100",
		_("Packing (Unit)") + ":Float:100",
		_("Currency") + "::100",
		_("Packing (Rate)") + ":Currency/Currency:120",
		_("Packing (Amount)") + ":Currency/Currency:150",
		_("Exchange Rate") + ":Currency:150",
		_("Amount (IDR)") + ":Currency:150",
		_("Warehouse") + ":Link/Warehouse:200",
		_("Cost Center") + ":Link/Cost Center:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_purhase_receipt(filters):
	conditions = get_conditions(filters)
	#return frappe.db.sql("""select item_name,item_group,stock_uom,expense_account,income_account,has_variants,is_purchase_item,is_sales_item,is_asset_item,is_sub_contracted_item from tabItem where has_variants = '0' and item_group = 'layanan' %s""" % conditions, as_list=1)
	#return frappe.db.sql("""select parent,item_code,item_name,item_group,packing_qty,packing_uom,conversion_factor,qty,stock_uom,rate,amount,warehouse,expense_account,cost_center,creation,owner,modified,modified_by from `tabDelivery Note Item` where docstatus < 2 %s""" % conditions, as_list=1)
	#return frappe.db.sql("""select `tabPurchase Receipt`.status,`tabPurchase Receipt`.name,`tabPurchase Receipt`.supplier,`tabPurchase Receipt`.company,`tabPurchase Receipt`.posting_date,`tabPurchase Receipt`.posting_time,`tabPurchase Receipt`.transporter_name,`tabPurchase Receipt`.lr_date,`tabPurchase Receipt`.lr_no,`tabPurchase Receipt`.currency,`tabPurchase Receipt`.price_list_currency,`tabPurchase Receipt`.conversion_rate,`tabPurchase Receipt`.base_net_total,concat(`tabCurrency`.symbol," ",`tabPurchase Receipt`.base_grand_total),`tabPurchase Receipt`.net_total,`tabPurchase Receipt`.base_total,`tabPurchase Receipt`.base_rounded_total from `tabPurchase Receipt` inner join `tabCurrency` on `tabPurchase Receipt`.currency = `tabCurrency`.name where `tabPurchase Receipt`.docstatus < 2 %s""" % conditions, as_list=1)
	return frappe.db.sql(
		"""select
				pr1.status,pr2.parent,pr1.posting_date,pr1.supplier,pr2.item_code,pr2.item_name,pr2.item_group,
				pr2.stock_qty,pr2.stock_uom,pr2.received_qty,
				pr2.qty,pr2.uom,pr2.conversion_factor,pr1.currency,
		        pr2.rate,pr2.amount,
				pr1.conversion_rate,pr2.base_amount,
				pr2.warehouse,pr2.cost_center,pr2.creation,
				pr2.owner,pr2.modified,pr2.modified_by
		   from
		   		`tabPurchase Receipt Item` pr2 inner join `tabPurchase Receipt` pr1

		   where
		   		pr2.parent = pr1.name and pr2.docstatus < 2 %s order by pr1.posting_date desc,pr1.posting_time desc,pr2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("purchase_receipt"):
		conditions += "and pr2.parent = '%s'" % filters["purchase_receipt"]

	if filters.get("item_group"):
		conditions += "and pr2.item_group = '%s'" % filters["item_group"]

	if filters.get("cost_center"):
		conditions += "and pr2.cost_center = '%s'" % filters["cost_center"]

	if filters.get("warehouse"):
		conditions += "and pr2.warehouse = '%s'" % filters["warehouse"]

	if filters.get("from_date"):
		conditions += "and pr1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and pr1.posting_date <= '%s'" % filters["to_date"]

	return conditions

	
