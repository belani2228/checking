# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _
import frappe.defaults

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	data = get_recheck_purchase_invoice_lcv(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("SupplierType") + "::80",
		_("No.Purchase Invoice")+":Link/Purchase Invoice:150",
		_("Supplier Inv") + ":Data:150",
		_("No.PU") + ":Data:150",
		_("Supplier Name") + ":Link/Supplier:300",
		_("PostingDate") + ":Date:100",
		_("Due Date") + ":Date:100",
		_("No.Document") + ":Data:120",
		_("DocumentDate") + ":Date:100",
		_("Currency") + ":Link/Currency:100",
		_("Amount") + ":Currency/Currency:120",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Outstanding Amount") + ":Currency/Currency:150",
		_("Expense Account") + ":Data:300",
		_("Payable Account") + ":Data:350",
		_("Remarks") + ":Data:350",
		_("CreatedDate") + ":Datetime:180",
		_("CreatedBy") + ":Data:200",
		_("ModifiedDate") + ":Datetime:180",
		_("ModifiedBy") + ":Data:200"
	]


def get_recheck_purchase_invoice_lcv(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select distinct
				if(pi2.due_date >= pi2.posting_date and pi2.docstatus = 1 and pi2.outstanding_amount = 0,"Paid",if(pi2.docstatus = 0,"Draft","Overdue")) as docstatuspi,
				s1.supplier_type,
				pi2.name,
				pi2.bill_no,
				pi2.pu_number,
				pi2.supplier,
				pi2.posting_date,
				pi2.due_date,
				pi2.bill_no,pi2.bill_date,
				pi2.currency,
				pi2.net_total,
				pi2.conversion_rate,
				pi2.base_total,
				pi2.outstanding_amount,
				pi2.against_expense_account,
				pi2.credit_to,
				pi2.remarks,
				pi2.creation,pi2.owner,
				pi2.modified,pi2.modified_by
		   from
		   		`tabPurchase Invoice` pi2
				inner join `tabSupplier` s1
				inner join `tabLanded Cost Taxes and Charges` lcv1
		   where
		   		pi2.supplier = s1.name
				and pi2.name = lcv1.get_from_purchase_invoice
		   		and pi2.docstatus < 2
				and pi2.is_opening = "No"
				and s1.supplier_type = "Service"
				and lcv1.get_from_purchase_invoice !=""
				%s
		   order by
		   		pi2.name desc,
				pi2.posting_date desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += "and pi2.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and pi2.posting_date <= '%s'" % filters["to_date"]

	if filters.get("purchase_invoice"):
		conditions += "and pi2.name = '%s'" % filters["purchase_invoice"]

	if filters.get("supplier"):
		conditions += "and pi2.supplier = '%s'" % filters["supplier"]

	if filters.get("recheck_month") == "If Posting Date > Created Date":
		conditions += "and (date(pi2.posting_date) > date(pi2.creation))"
	elif filters.get("recheck_month") == "If Posting Date < Created Date":
		conditions += "and (date(pi2.posting_date) < date(pi2.creation))"
	elif filters.get("recheck_month") == "If Posting Date > Document Date":
		conditions += "and (date(pi2.posting_date) > date(pi2.bill_date))"
	elif filters.get("recheck_month") == "If Posting Date < Document Date":
		conditions += "and (date(pi2.posting_date) < date(pi2.bill_date))"
	elif filters.get("recheck_month") == "Posting Date (Year) > Document Date (Year)":
		if filters.get("from_date") is not None or filters.get("to_date") is not None:
			frappe.throw(_("please, don't fill from date  and to date"))

		conditions += "and (year(pi2.posting_date) > year(pi2.bill_date))"
	elif filters.get("recheck_month") == "Posting Date (Year) > Created Date (Year)":
		if filters.get("from_date") is not None or filters.get("to_date") is not None:
			frappe.throw(_("please, don't fill from date  and to date"))

		conditions += "and (year(pi2.posting_date) > year(pi2.creation))"

	else:
		conditions += ""

	if filters.get("entry_type") == "Draft":
		conditions += "and pi2.docstatus = '0'"
	elif filters.get("entry_type") == "Paid":
		conditions += "and pi2.docstatus = '1' and pi2.outstanding_amount = '0'"
	elif filters.get("entry_type") == "Overdue":
		conditions += "and pi2.docstatus = '1' and pi2.outstanding_amount != '0'"
	else:
		conditions += "and (pi2.docstatus = '1' or pi2.docstatus = '0')"
	return conditions
