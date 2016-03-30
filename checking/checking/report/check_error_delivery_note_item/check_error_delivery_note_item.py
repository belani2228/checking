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
	    _("Status (DN)") + ":Data:100",
		_("Status (SI)") + ":Data:100",
		_("No.Delivery Note")+":Link/Delivery Note:110",
		_("No.Sales Invoice")+":Link/Sales Invoice:110",
		_("Posting Date (DN)") + ":Date:150",
		_("Posting Time (DN)") + ":Time:150",
		_("Posting Date (SI)") + ":Date:150",
		_("Posting Time (SI)") + ":Time:150",
		_("Customer Name (DN)") + ":Link/Customer:250",
		_("Customer Name (SI)") + ":Link/Customer:250",
		_("ITEM (DN)") + ":Link/Item:250",
		_("ITEM (SI)") + ":Link/Item:250",
		_("Warehouse (DN)") + ":Link/Warehouse:150",
		_("Warehouse (SI)") + ":Link/Warehouse:150",
		_("Cost Center (DN)") + ":Link/Cost Center:150",
		_("Cost Center (SI)") + ":Link/Cost Center:150",
		_("Created Date (DN)") + ":Datetime:150",
		_("Created By (DN)") + ":Data:200",
		_("Created Date (SI)") + ":Datetime:150",
		_("Created By (SI)") + ":Data:200",
		_("Modified Date (DN)") + ":Datetime:150",
		_("Modified By (DN)") + ":Data:200",
		_("Modified Date (SI)") + ":Datetime:150",
		_("Modified By (SI)") + ":Data:200"
	]

def get_recheck_delivery_note(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select distinct
				dn1.status,
				if(si1.due_date >= si1.posting_date and si1.docstatus = 1 and si1.outstanding_amount = 0,"Paid",if(si1.docstatus = 0,"Draft","Overdue")) as docstatussi,
				dn2.parent,
				si2.parent,
				dn1.posting_date,
				dn1.posting_time,
				si1.posting_date,
				si1.posting_time,
				dn1.customer,
				si1.customer,
				dn2.item_code,
				si2.item_code,
				dn2.warehouse,
				si2.warehouse,
				dn2.cost_center,
				si2.cost_center,
				dn2.creation,
				dn2.owner,
				si2.creation,
				si2.owner,
				dn2.modified,
				dn2.modified_by,
				si2.modified,
				si2.modified_by
		   from
		   		`tabDelivery Note Item` dn2
				inner join `tabDelivery Note` dn1
				inner join `tabSales Invoice` si1
				inner join `tabSales Invoice Item` si2
		   where
		   		dn2.parent = dn1.name
				and dn2.docstatus < 2
				and si2.docstatus < 2
				and dn2.name = si2.dn_detail
				and si1.name = si2.parent
				%s
		  order by
		  		dn1.posting_date desc,
				dn1.posting_time desc,
				dn2.parent desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += "and dn1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and dn1.posting_date <= '%s'" % filters["to_date"]

	if filters.get("recheck_group") == "Posting Date DN-SI":
		conditions += "and ((dn1.posting_date > si1.posting_date) and (dn1.posting_time > si1.posting_time))"

	elif filters.get("recheck_group") == "Customer DN-SI":
		conditions += "and (dn1.customer <> si1.customer)"

	elif filters.get("recheck_group") == "Cost Center DN-SI":
		conditions += "and (dn2.cost_center <> si2.cost_center)"

	elif filters.get("recheck_group") == "Warehouse DN-SI":
		conditions += "and (dn2.warehouse <> si2.warehouse)"

	else:
		conditions += "and (dn2.item_code <> si2.item_code)"

	return conditions
