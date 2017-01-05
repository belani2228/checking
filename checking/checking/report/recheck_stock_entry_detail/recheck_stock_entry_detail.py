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
	data = get_recheck_stock_entry_detail(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("Project") + "::100",
		_("Document") + "::120",
		_("No.Stock Entry") + ":Link/Stock Entry:100",
		_("Amended From") + ":Link/Stock Entry:100",
		_("PostingDate") + ":Date:100",
		_("Cost Center") + ":Data:200",
		_("Source Warehouse") + ":Data:220",
		_("Target Warehouse") + ":Data:220",
		_("Item Name") + ":Data:350",
		_("Packing Qty") + ":Float:100",
		_("Packing UOM") + ":Data:100",
		_("Conversion") + ":Float:80",
		_("Actual Qty") + ":Float:100",
		_("Stock UOM") + ":Data:80",
		_("BasicRate") + ":Currency:120",
		_("ValuationRate") + ":Currency:120",
		_("Basic Amount") + ":Currency:120",
		_("AdditionalCost") + ":Currency:120",
		_("Amount") + ":Currency:120",
		_("Expense Account") + ":Data:200",
		_("CreatedDate") + ":Datetime:180",
		_("CreatedBy") + ":Data:200",
		_("ModifiedDate") + ":Datetime:180",
		_("ModifiedBy") + ":Data:200"
	]

def get_recheck_stock_entry_detail(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
		        if(st1.docstatus = 0,"Draft","Submitted"),
				st1.project,
				st1.purpose,
			    st1.name,
				st1.amended_from,
				st1.posting_date,
				st2.cost_center,
				st2.s_warehouse,
				st2.t_warehouse,
				st2.item_name,
				st2.packing_qty,
				st2.packing_uom,
				st2.conversion_factor,
				st2.actual_qty,
				st2.stock_uom,
				st2.basic_rate,
				st2.valuation_rate,
				st2.basic_amount,
				st2.additional_cost,
				st2.amount,
				st2.expense_account,
				st2.creation,st2.owner,
				st2.modified,st2.modified_by
		   from
		   		`tabStock Entry Detail` st2
				 inner join `tabStock Entry` st1
		   where
		   		st1.name = st2.parent and
				st1.docstatus < 2 %s
		   order by
		   		st1.posting_date desc,st1.posting_time desc, st1.name desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		conditions += "and st1.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and st1.posting_date <= '%s'" % filters["to_date"]

	if filters.get("stock_entry"):
		conditions += "and st1.name = '%s'" % filters["stock_entry"]

	if filters.get("cost_center"):
		conditions += "and st2.cost_center = '%s'" % filters["cost_center"]

	if filters.get("purpose") == "Material Issue":
		conditions += "and st1.purpose = 'Material Issue'"
	elif filters.get("purpose") == "Material Receipt":
		conditions += "and st1.purpose = 'Material Receipt'"
	elif filters.get("purpose") == "Material Transfer":
		conditions += "and st1.purpose = 'Material Transfer'"
	elif filters.get("purpose") == "Repack":
		conditions += "and st1.purpose = 'Repack'"
	elif filters.get("purpose") == "Subcontract":
		conditions += "and st1.purpose = 'Subcontract'"
	elif filters.get("purpose") == "Manufacture":
		conditions += "and st1.purpose = 'Manufacture'"
	elif filters.get("purpose") == "Material Transfer for Manufacture":
			conditions += "and st1.purpose = 'Material Transfer for Manufacture'"
	else:
		conditions += ""

	if filters.get("entry_type") == "Draft":
		conditions += "and st1.docstatus = '0'"
	elif filters.get("entry_type") == "Submitted":
		conditions += "and st1.docstatus = '1'"
	else:
		conditions += ""

	return conditions
