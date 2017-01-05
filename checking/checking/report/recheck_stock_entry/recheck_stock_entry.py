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
	data = get_recheck_stock_entry(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("Project") + "::100",
		_("Document") + "::150",
		_("No.Stock Entry") + ":Link/Stock Entry:100",
		_("Amended From") + ":Link/Stock Entry:100",
		_("PostingDate") + ":Date:100",
		_("Source Warehouse") + ":Data:200",
		_("Target Warehouse") + ":Data:200",
		_("TotalIncomingValue") + ":Currency:150",
		_("TotalOutcomingValue") + ":Currency:150",
		_("TotalAdditionalCosts") + ":Currency:150",
		_("TotalValueDifference") + ":Currency:150",
		_("TotalAmount") + ":Currency:120",
		_("Remarks") + ":Data:500",
		_("CreatedDate") + ":Datetime:180",
		_("CreatedBy") + ":Data:200",
		_("ModifiedDate") + ":Datetime:180",
		_("ModifiedBy") + ":Data:200"
	]

def get_recheck_stock_entry(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
		        if(docstatus = 0,"Draft","Submitted"),
				project,
				purpose,
			    name,
				amended_from,
				posting_date,
				from_warehouse,
				to_warehouse,
				total_incoming_value,
				total_outgoing_value,
				total_additional_costs,
				value_difference,
				total_amount,
				remarks,
				creation,owner,
				modified,modified_by
		   from
		   		`tabStock Entry`
		   where
		   		docstatus < 2 %s
		   order by
		   		posting_date desc,posting_time desc, name desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		conditions += "and posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and posting_date <= '%s'" % filters["to_date"]

	if filters.get("stock_entry"):
		conditions += "and name = '%s'" % filters["stock_entry"]

	if filters.get("purpose") == "Material Issue":
		conditions += "and purpose = 'Material Issue'"
	elif filters.get("purpose") == "Material Receipt":
		conditions += "and purpose = 'Material Receipt'"
	elif filters.get("purpose") == "Material Transfer":
		conditions += "and purpose = 'Material Transfer'"
	elif filters.get("purpose") == "Repack":
		conditions += "and purpose = 'Repack'"
	elif filters.get("purpose") == "Subcontract":
		conditions += "and purpose = 'Subcontract'"
	elif filters.get("purpose") == "Manufacture":
		conditions += "and purpose = 'Manufacture'"
	elif filters.get("purpose") == "Material Transfer for Manufacture":
			conditions += "and purpose = 'Material Transfer for Manufacture'"
	else:
		conditions += ""

	if filters.get("entry_type") == "Draft":
		conditions += "and docstatus = '0'"
	elif filters.get("entry_type") == "Submitted":
		conditions += "and docstatus = '1'"
	else:
		conditions += ""

	return conditions
