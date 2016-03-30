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
		_("Statuxs") + ":Data:80",
		_("No.Puchase Receipt")+":Link/Purchase Receipt:150",
		_("No.Puchase Invoice")+":Link/Purchase Invoice:150",
		_("Posting Date (PR)") + ":Date:150",
		_("Posting Date (PI)") + ":Date:150",
		_("Supplier Name (PR)") + ":Link/Supplier:250",
		_("Supplier Name (PI)") + ":Link/Supplier:250",
		_("Cost Center (PR)") + ":Link/Cost Center:250",
		_("Cost Center (PI)") + ":Link/Cost Center:250",
		_("Created Date (PR)") + ":Datetime:150",
		_("Created By (PR)") + ":Data:200",
		_("Created Date (PI)") + ":Datetime:150",
		_("Created By (PI)") + ":Data:200",
		_("Modified Date (PR)") + ":Datetime:150",
		_("Modified By (PR)") + ":Data:200",
		_("Modified Date (PI)") + ":Datetime:150",
		_("Modified By (PI)") + ":Data:200"
	]

def get_recheck_purhase_receipt(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select distinct
				pr1.status,
				if(pi1.due_date >= pi1.posting_date and pi1.docstatus = 1 and pi1.outstanding_amount = 0,"Paid",if(pi1.docstatus = 0,"Draft","Overdue")) as docstatuspi,
				pr2.parent,
				pi2.parent,
				pr1.posting_date,
				pi1.posting_date,
				pr1.supplier,
				pi1.supplier,
				pr2.cost_center,
				pi2.cost_center,
				pr2.creation,pr2.owner,
				pi2.creation,pi2.owner,
				pr2.modified,pr2.modified_by,
				pi2.modified,pi2.modified_by
		   from
		   		`tabPurchase Receipt Item` pr2
				inner join `tabPurchase Receipt` pr1
				inner join `tabPurchase Invoice` pi1
				inner join `tabPurchase Invoice Item` pi2

		   where
		   		pr2.parent = pr1.name
				and pr2.docstatus < 2
				and pi2.docstatus < 2
				and pr2.name = pi2.pr_detail
				and pi1.name = pi2.parent
				 %s

			order by
				pr1.posting_date desc,
				pr2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		conditions += "and pr1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and pr1.posting_date <= '%s'" % filters["to_date"]

	if filters.get("recheck_group") == "Posting Date PR-PI":
		conditions += "and (pr1.posting_date > pi1.posting_date)"

	elif filters.get("recheck_group") == "Supplier PR-PI":
		conditions += "and (pr1.supplier <> pi1.supplier)"

	elif filters.get("recheck_group") == "Cost Center PR-PI":
		conditions += "and (pr2.cost_center <> pi2.cost_center)"

	else:
		conditions += "and (pr2.item_code <> pi2.item_code)"
	return conditions
