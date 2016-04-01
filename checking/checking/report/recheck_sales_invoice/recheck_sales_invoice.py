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
	data = get_recheck_sales_invoice(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("Customer Group") + ":Link/Customer Group:100",
		_("No.Sales Invoice")+":Link/Sales Invoice:100",
		_("Customer Name") + ":Link/Customer:300",
		_("Territory") + ":Link/Territory:100",
		_("Posting Date") + ":Date:100",
		_("Due Date") + ":Date:100",
		#_("No.Document") + ":Data:120",
		#_("Document Date") + ":Date:100",
		_("Currency") + ":Link/Currency:80",
		_("Amount") + ":Currency/Currency:120",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Amount (IDR) Rounded") + ":Currency:150",
		_("Outstanding Amount") + ":Currency/Currency:150",
		_("Income Account") + "::180",
		_("Receivable Account") + "::250",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_sales_invoice(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(si2.due_date >= si2.posting_date and si2.docstatus = 1 and si2.outstanding_amount = 0,"Paid",if(si2.docstatus = 0,"Draft","Overdue")) as docstatussi,
				c1.customer_group,
				si2.name,si2.customer,
				si2.territory,
				si2.posting_date,
				si2.due_date,
				si2.currency,
				si2.net_total,
				si2.conversion_rate,
				si2.base_total,
				si2.base_rounded_total,
				si2.outstanding_amount,
				si2.against_income_account,
				si2.debit_to,
				si2.creation,si2.owner,
				si2.modified,si2.modified_by
		   from
		   		`tabSales Invoice` si2 inner join `tabCustomer` c1
		   where
		   		si2.customer = c1.name
		   		and si2.docstatus < 2
				and si2.is_opening = "No" %s
		   order by
		   		si2.name desc,
				si2.posting_date desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and si2.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):

		#conditions += "and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
		conditions += "and si2.posting_date <= '%s'" % filters["to_date"]

	if filters.get("sales_invoice"):
		conditions += "and si2.name = '%s'" % filters["sales_invoice"]

	if filters.get("customer_group"):
		conditions += "and c1.customer_group = '%s'" % filters["customer_group"]

	if filters.get("customer"):
		conditions += "and si2.customer = '%s'" % filters["customer"]

	if filters.get("territory"):
		conditions += "and si2.territory = '%s'" % filters["territory"]

	if filters.get("entry_type") == "Draft":
		conditions += "and si2.docstatus = '0'"
	elif filters.get("entry_type") == "Paid":
		conditions += "and si2.docstatus = '1' and si2.outstanding_amount = '0'"
	elif filters.get("entry_type") == "Overdue":
		conditions += "and si2.docstatus = '1' and si2.outstanding_amount != '0'"
	else:
		conditions += "and (si2.docstatus = '1' or si2.docstatus = '0')"

	return conditions
