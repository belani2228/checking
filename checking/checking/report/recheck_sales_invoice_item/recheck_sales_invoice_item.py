# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_sales_invoice_item(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("Customer Group") + "::120",
		_("No.Sales Invoice")+":Link/Sales Invoice:120",
		_("Remarks")+":Data:80",
		_("Posting Date") + ":Date:100",
		_("Customer Name") + ":Link/Customer:200",
		_("Item Code") + ":Link/Item:300",
		_("Item Name") + "::300",
		_("Item Group") + ":Link/Item Group:120",
		_("Packing (QTY)") + ":Float:100",
		_("Packing (UoM)") + "::100",
		_("Packing (Unit)") + ":Float:100",
		_("QTY") + ":Float:100",
		_("UoM") + "::100",
		_("Rate") + ":Currency/Currency:120",
		#_("Packing (Amount)") + ":Currency/Currency:150",
		#_("C") + ":Currency:150",
		_("Amount (IDR)") + ":Currency:150",
		_("Warehouse") + ":Link/Warehouse:200",
		_("Cost Center") + ":Link/Cost Center:150",
		_("Delivery Note") + ":Link/Delivery Note:100",
		_("Expense Account") + "::200",
		_("Income Account") + "::200",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_sales_invoice_item(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(si1.due_date >= si1.posting_date and si1.docstatus = 1 and si1.outstanding_amount = 0,"Paid",if(si1.docstatus = 0,"Draft","Overdue")) as docstatussi,
				c1.customer_group,
				si2.parent,
				si1.remarks,
				si1.posting_date,
				si1.customer,
				si2.item_code,
				si2.item_name,
				si2.item_group,
				si2.packing_qty,
				si2.packing_uom,
				si2.conversion_factor,
				si2.qty,
				si2.stock_uom,

				si2.rate,
				si2.amount,
				si2.warehouse,
				si2.cost_center,
				si2.delivery_note,
				si2.expense_account,
				si2.income_account,
				si2.creation,
				si2.owner,
				si2.modified,
				si2.modified_by
		   from
		   		`tabSales Invoice Item` si2
				inner join `tabSales Invoice` si1
				inner join `tabCustomer` c1
		   where
		   		si2.parent = si1.name
				and c1.name = si1.customer
				and si1.docstatus <2
				and si2.docstatus < 2
				and si1.is_opening = "No"%s
		   order by
		   		si1.posting_date desc,
				si2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("sales_invoice"):
		conditions += "and si2.parent = '%s'" % filters["sales_invoice"]

	if filters.get("item_group"):
		conditions += "and si2.item_group = '%s'" % filters["item_group"]

	if filters.get("cost_center"):
		conditions += "and si2.cost_center = '%s'" % filters["cost_center"]

	if filters.get("customer"):
		conditions += "and si1.customer = '%s'" % filters["customer"]

	if filters.get("customer_group"):
		conditions += "and c1.customer_group = '%s'" % filters["customer_group"]

	if filters.get("from_date"):
		conditions += "and si1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and si1.posting_date <= '%s'" % filters["to_date"]

    #----------------------recheck entry type-----------------------------------
	if filters.get("entry_type") == "Draft":
		conditions += "and si1.docstatus = '0'"
	elif filters.get("entry_type") == "Paid":
		conditions += "and si1.docstatus = '1' and si1.outstanding_amount = '0'"
	elif filters.get("entry_type") == "Overdue":
		conditions += "and si1.docstatus = '1' and si1.outstanding_amount != '0'"
	else:
		conditions += "and (si1.docstatus = '1' or si1.docstatus = '0')"

    #----------------------recheck customer-----------------------------------
 	if ((filters.get("customer_group") is not None) and (filters.get("recheck_customer") is not None)) :
		 frappe.throw(_("please, don't fill 'customer group' filter if you use 'Recheck customer use wrong warehouse' filter"))

    #----------------------recheck customer-----------------------------------
	if filters.get("recheck_customer") == "Customer Buah-Jkt":
		conditions += "and si1.customer_group = 'Buah-Dadap' and si2.warehouse != 'Gudang Buah - Dadap - ABC'"
	elif filters.get("recheck_customer") == "Customer Bawang-Jkt":
		conditions += "and si1.customer_group = 'Bawang-Dadap' and si2.warehouse != 'Gudang Bawang - Dadap - ABC'"
	elif filters.get("recheck_customer") == "Customer AKS-Sby":
		conditions += "and (si1.customer_group = 'Pios' or si1.customer_group = 'Puspa' or si1.customer_group = 'Suri' or si1.customer_group = 'Songoyudan') and (si2.warehouse = 'Gudang Bawang - Dadap - ABC' or si2.warehouse = 'Gudang Buah - Dadap - ABC')"
	else:
		conditions += ""

	return conditions
