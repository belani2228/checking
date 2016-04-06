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
	data = get_recheck_purchase_invoice(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("SupplierType") + "::80",
		_("No.Purchase Invoice")+":Link/Purchase Invoice:150",
		_("Supplier Name") + ":Link/Supplier:300",
		_("Posting Date") + ":Date:100",
		_("Due Date") + ":Date:100",
		_("No.Document") + ":Data:120",
		_("Document Date") + ":Date:100",
		_("Currency") + "::100",
		_("Amount") + ":Currency/Currency:120",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Outstanding Amount") + ":Currency/Currency:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]


def get_recheck_purchase_invoice(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(pi2.due_date >= pi2.posting_date and pi2.docstatus = 1 and pi2.outstanding_amount = 0,"Paid",if(pi2.docstatus = 0,"Draft","Overdue")) as docstatuspi,
				s1.supplier_type,
				pi2.name,pi2.supplier,
				pi2.posting_date,
				pi2.due_date,
				pi2.bill_no,pi2.bill_date,
				pi2.currency,
				pi2.net_total,
				pi2.conversion_rate,
				pi2.base_total,
				pi2.outstanding_amount,
				pi2.creation,pi2.owner,
				pi2.modified,pi2.modified_by
		   from
		   		`tabPurchase Invoice` pi2 inner join `tabSupplier` s1
		   where
		   		pi2.supplier = s1.name
		   		and pi2.docstatus < 2
				and pi2.is_opening = "No" %s
		   order by
		   		pi2.name desc,
				pi2.posting_date desc
		""" % conditions, as_list=1)
	#return frappe.db.sql("""select `tabPurchase Receipt`.status,`tabPurchase Receipt`.name,`tabPurchase Receipt`.supplier,`tabPurchase Receipt`.company,`tabPurchase Receipt`.posting_date,`tabPurchase Receipt`.posting_time,`tabPurchase Receipt`.transporter_name,`tabPurchase Receipt`.lr_date,`tabPurchase Receipt`.lr_no,`tabPurchase Receipt`.currency,`tabPurchase Receipt`.price_list_currency,`tabPurchase Receipt`.conversion_rate,`tabPurchase Receipt`.base_net_total,concat(`tabCurrency`.symbol," ",`tabPurchase Receipt`.base_grand_total),`tabPurchase Receipt`.net_total,`tabPurchase Receipt`.base_total,`tabPurchase Receipt`.base_rounded_total from `tabPurchase Receipt` inner join `tabCurrency` on `tabPurchase Receipt`.currency = `tabCurrency`.name where `tabPurchase Receipt`.docstatus < 2 %s""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and pi2.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):

		#conditions += "and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
		conditions += "and pi2.posting_date <= '%s'" % filters["to_date"]

	if filters.get("purchase_invoice"):
		conditions += "and pi2.name = '%s'" % filters["purchase_invoice"]

	if filters.get("supplier_type"):
		conditions += "and s1.supplier_type = '%s'" % filters["supplier_type"]

	if filters.get("supplier"):
		conditions += "and pi2.supplier = '%s'" % filters["supplier"]

	if filters.get("entry_type") == "Draft":
		conditions += "and pi2.docstatus = '0'"
	elif filters.get("entry_type") == "Paid":
		conditions += "and pi2.docstatus = '1' and pi2.outstanding_amount = '0'"
	elif filters.get("entry_type") == "Overdue":
		conditions += "and pi2.docstatus = '1' and pi2.outstanding_amount != '0'"
	else:
		conditions += "and (pi2.docstatus = '1' or pi2.docstatus = '0')"
	return conditions
