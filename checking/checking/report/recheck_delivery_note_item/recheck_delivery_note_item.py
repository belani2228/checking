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

	if filters.get("entry_type") == "Draft":
		conditions += "and dn1.docstatus = '0' and dn1.is_return = '0'"
	elif filters.get("entry_type") == "To Bill":
		conditions += "and dn1.docstatus = '1' and dn1.is_return = '0' and dn1.per_billed < '100'"
	elif filters.get("entry_type") == "Completed":
		conditions += "and dn1.docstatus = '1' and dn1.is_return = '0' and dn1.per_billed = '100'"
	elif filters.get("entry_type") == "Return":
		conditions += "and dn1.is_return = '1'"
	else:
		conditions += "and dn1.per_billed <= '100'"

  #----------------------recheck warehouse-----------------------------------
	if ((filters.get("recheck_warehouse") is not None) and (filters.get("warehouse") is not None)) :
		 frappe.throw(_("please, don't fill 'warehouse' filter if you use 'recheck warehouse if input wrong cost center' filter"))

  #----------------------recheck warehouse-----------------------------------
	if filters.get("recheck_warehouse") == "Gudang Buah-Dadap":
		conditions += "and (dn2.warehouse = 'Gudang Buah - Dadap - ABC' and dn2.cost_center != 'Buah/Jakarta - ABC')"
	elif filters.get("recheck_warehouse") == "Gudang Bawang-Dadap":
		conditions += "and (dn2.warehouse = 'Gudang Bawang - Dadap - ABC' and dn2.cost_center != 'Bawang/Jakarta - ABC')"
	elif filters.get("recheck_warehouse") == "Gudang Suri":
		conditions += "and (dn2.warehouse = 'Gudang Suri - ABC' and dn2.cost_center != 'AKS Gudang - ABC') and (dn2.warehouse = 'Gudang Suri - ABC' and dn2.cost_center != 'Sarden - ABC')"
	elif filters.get("recheck_warehouse") == "Toko Puspa":
		conditions += "and (dn2.warehouse = 'Toko Puspa - ABC' and dn2.cost_center != 'Puspa Toko - ABC')"
	elif filters.get("recheck_warehouse") == "Toko Pios":
		conditions += "and (dn2.warehouse = 'Toko Pios - ABC' and dn2.cost_center != 'Pios Toko - ABC')"
	elif filters.get("recheck_warehouse") == "Toko Songoyudan":
		conditions += "and (dn2.warehouse = 'Toko Songoyudan - ABC' and dn2.cost_center != 'Songoyudan Toko - ABC')"
	elif filters.get("recheck_warehouse") == "Gudang Pios":
		conditions += "and (dn2.warehouse = 'Gudang Pios - ABC' and dn2.cost_center != 'AKS Gudang - ABC')"
	else:
		conditions += ""

   #----------------------recheck customer-----------------------------------
   	if filters.get("recheck_customer") == "Customer Buah-Jkt":
		conditions += "and dn1.customer_group = 'Buah-Dadap' and dn2.warehouse != 'Gudang Buah - Dadap - ABC'"

	elif filters.get("recheck_customer") == "Customer Bawang-Jkt":
		conditions += "and dn1.customer_group = 'Bawang-Dadap' and dn2.warehouse != 'Gudang Bawang - Dadap - ABC'"

	elif filters.get("recheck_customer") == "Customer AKS-Sby":
		conditions += "and (dn1.customer_group = 'Pios' or dn1.customer_group = 'Puspa' or dn1.customer_group = 'Suri' or dn1.customer_group = 'Songoyudan') and (dn2.warehouse = 'Gudang Bawang - Dadap - ABC' or dn2.warehouse = 'Gudang Buah - Dadap - ABC')"

	else:
		conditions += ""

	return conditions
