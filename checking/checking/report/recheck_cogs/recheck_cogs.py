# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, fmt_money
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_cogs(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("Document") + "::120",
		_("No.Puchase Receipt")+":Link/Purchase Receipt:140",
		_("No.PU") + ":Data:120",
		_("No.Vehicle") + ":Data:120",
		_("Posting Date") + ":Date:100",
		_("Supplier Name") + ":Link/Supplier:200",
		_("SupplierType") + ":Data:100",
		_("Item Code") + ":Link/Item:300",
		_("Item Name") + "::300",
		_("Qty") + ":Float:80",
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
		_("LCVAmountIDR") + ":Currency:150",
		_("COGS Amount (IDR)") + ":Currency:150",
		_("COGS Amount/QTY (IDR)") + ":Currency:180",
		_("Warehouse") + ":Link/Warehouse:200",
		_("Item Group") + ":Link/Item Group:100",
		_("Cost Center") + ":Link/Cost Center:150"

	]

def get_recheck_cogs(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
	"""select
			pr1.status,
			if(is_return = 1,"Return","Purchase Receipt"),
			pr2.parent,pr1.pu_number,pr1.lr_no,pr1.posting_date,pr1.supplier,s1.supplier_type,pr2.item_code,pr2.item_name,
			pr2.stock_qty,pr2.stock_uom,pr2.received_qty,
			pr2.qty,pr2.uom,pr2.conversion_factor,pr1.currency,
			pr2.rate,pr2.amount,
			pr1.conversion_rate,pr2.base_amount,pr2.landed_cost_voucher_amount,
			(pr2.landed_cost_voucher_amount + pr2.base_amount) as grandtotalxd,
			((pr2.landed_cost_voucher_amount + pr2.base_amount) / pr2.stock_qty) as grandtotalxd1,
			pr2.warehouse,pr2.item_group,pr2.cost_center
	   from
			`tabPurchase Receipt Item` pr2 inner join `tabPurchase Receipt` pr1 inner join `tabSupplier` s1
	   where
			pr2.parent = pr1.name and s1.name = pr1.supplier and pr2.docstatus < 2 %s order by pr1.posting_date desc,pr1.posting_time desc,pr2.parent desc
	""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("purchase_receipt"):
		conditions += "and pr2.parent = '%s'" % filters["purchase_receipt"]
	if filters.get("item_group"):
		conditions += "and pr2.item_group = '%s'" % filters["item_group"]
	if filters.get("warehouse"):
		conditions += "and pr2.warehouse = '%s'" % filters["warehouse"]
	if filters.get("from_date"):
		conditions += "and pr1.posting_date >= '%s'" % filters["from_date"]
	if filters.get("to_date"):
		conditions += "and pr1.posting_date <= '%s'" % filters["to_date"]
	if filters.get("entry_type") == "Draft":
		conditions += "and pr1.docstatus = '0' and pr1.is_return = '0'"
	elif filters.get("entry_type") == "To Bill":
		conditions += "and pr1.docstatus = '1' and pr1.is_return = '0' and pr1.per_billed < '100'"
	elif filters.get("entry_type") == "Completed":
		conditions += "and pr1.docstatus = '1' and pr1.is_return = '0' and pr1.per_billed = '100'"
	elif filters.get("entry_type") == "Return":
		conditions += "and pr1.is_return = '1'"
	else:
		conditions += "and pr1.per_billed <= '100'"
	return conditions
