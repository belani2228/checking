# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_purchase_invoice_item(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("Project") + "::100",
		_("SupplierType") + "::80",
		_("No.Puchase Invoice")+":Link/Purchase Invoice:120",
		_("Supplier Inv") + ":Data:150",
		_("No.PU") + ":Data:120",
		_("Posting Date") + ":Date:100",
		_("Supplier Name") + ":Link/Supplier:200",
		_("Item Code") + ":Link/Item:300",
		_("Item Name") + "::300",
		_("Item Group") + ":Link/Item Group:100",
		_("Packing (QTY)") + ":Float:100",
		_("Packing (UoM)") + "::100",
		_("Packing (Unit)") + ":Float:100",
		_("Currency") + "::100",
		_("Packing (Rate)") + ":Currency/Currency:120",
		_("Packing (Amount)") + ":Currency/Currency:150",
		_("Exchange Rate") + ":Currency:150",
		_("Amount (IDR)") + ":Currency:150",
		_("No.Container") + "::100",
		_("Cost Center") + ":Link/Cost Center:100",
		_("Purchase Receipt") + ":Link/Purchase Receipt:100",
		_("Expense Account") + "::300",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_purchase_invoice_item(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(pi1.due_date >= pi1.posting_date and pi1.docstatus = 1 and pi1.outstanding_amount = 0,"Paid",if(pi1.docstatus = 0,"Draft","Overdue")) as docstatuspi,
				pi2.project,
				s1.supplier_type,
				pi2.parent,
				pi1.bill_no,
				pi1.pu_number,
				pi1.posting_date,
				pi1.supplier,
				pi2.item_code,
				pi2.item_name,
				pi2.item_group,
				pi2.qty,
				pi2.uom,
				pi2.conversion_factor,
				pi1.currency,
		        pi2.rate,
				pi2.amount,
				pi1.conversion_rate,
				pi2.base_amount,
				pi2.container,
				pi2.cost_center,
				pi2.purchase_receipt,
				pi2.expense_account,
				pi2.creation,
				pi2.owner,
				pi2.modified,
				pi2.modified_by
		   from
		   		`tabPurchase Invoice Item` pi2
				inner join `tabPurchase Invoice` pi1
				inner join `tabSupplier` s1
		   where
		   		pi2.parent = pi1.name
				and s1.name = pi1.supplier
				and pi1.docstatus <2
				and pi2.docstatus < 2
				and pi1.is_opening = "No"%s
		   order by
		   		pi1.posting_date desc,
				pi2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("purchase_invoice"):
		conditions += "and pi2.parent = '%s'" % filters["purchase_invoice"]

	if filters.get("item_group"):
		conditions += "and pi2.item_group = '%s'" % filters["item_group"]

	if filters.get("cost_center"):
		conditions += "and pi2.cost_center = '%s'" % filters["cost_center"]

	if filters.get("supplier"):
		conditions += "and pi1.supplier = '%s'" % filters["supplier"]

	if filters.get("supplier_type"):
		conditions += "and s1.supplier_type = '%s'" % filters["supplier_type"]

	if filters.get("from_date"):
		conditions += "and pi1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and pi1.posting_date <= '%s'" % filters["to_date"]

	if filters.get("entry_type") == "Draft":
		conditions += "and pi1.docstatus = '0'"
	elif filters.get("entry_type") == "Paid":
		conditions += "and pi1.docstatus = '1' and pi1.outstanding_amount = '0'"
	elif filters.get("entry_type") == "Overdue":
		conditions += "and pi1.docstatus = '1' and pi1.outstanding_amount != '0'"
	else:
		conditions += "and (pi1.docstatus = '1' or pi1.docstatus = '0')"

	return conditions
