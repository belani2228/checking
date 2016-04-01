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
		_("No.LCV")+":Link/Landed Cost Voucher:100",
		_("No.PI-LCV") + ":Link/Purchase Invoice:100",
		_("Description") + "::300",
		_("Amount (IDR)") + ":Currency:120",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]


def get_recheck_purchase_invoice_lcv(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(lcv1.docstatus = 0,"Draft","Submit"),
				lcv1.name,
				lcv3.get_from_purchase_invoice,
				lcv3.description,
				lcv3.amount,
				lcv3.creation,lcv3.owner,
				lcv3.modified,lcv3.modified_by
		   from
				`tabLanded Cost Taxes and Charges` lcv3
				inner join `tabLanded Cost Voucher` lcv1
		   where
		   		lcv1.name = lcv3.parent
				and lcv1.docstatus < 2
				and lcv3.get_from_purchase_invoice = ""
				%s
		   order by
		   		lcv1.name desc,lcv1.modified desc,lcv1.creation desc

		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""

	if filters.get("landed_cost_voucher"):
		conditions += "and lcv1.name = '%s'" % filters["landed_cost_voucher"]

	if filters.get("from_date"):
		conditions += "and lcv1.modified >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and lcv1.modified <= '%s'" % filters["to_date"]

	return conditions
