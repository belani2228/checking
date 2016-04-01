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
	data = get_recheck_journal_entry(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("Voucher Type") + "::100",
		_("No.Journal Entry")+":Link/Journal Entry:150",
		_("Posting Date") + ":Date:100",
		_("No.Document") + ":Data:120",
		_("Document Date") + ":Date:100",
		_("Remarks") + "::300",
		_("Debit") + ":Currency/Currency:120",
		_("Credit") + ":Currency/Currency:120",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_journal_entry(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(jv1.docstatus = '1',"Submit","Draft") as docstatusjv,
				jv1.voucher_type,
				jv1.name,
				jv1.posting_date,
				jv1.cheque_no,
				jv1.cheque_date,
				jv1.user_remark,
				jv1.total_debit,
				jv1.total_credit,
				jv1.creation,jv1.owner,
				jv1.modified,jv1.modified_by
		   from
		   		`tabJournal Entry` jv1
		   where
		   		jv1.docstatus < 2
				and jv1.is_opening = 'No'
				%s
		   order by
		   		jv1.name desc, jv1.posting_date desc

		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""

	if filters.get("entry_document") == "Draft":
		conditions += "and jv1.docstatus = '0'"
	elif filters.get("entry_document") == "Submit":
		conditions += "and jv1.docstatus = '1'"
	else:
		conditions += ""

	if filters.get("from_date"):
		conditions += "and jv1.posting_date >= '%s'" % filters["from_date"]
	if filters.get("to_date"):
		conditions += "and jv1.posting_date <= '%s'" % filters["to_date"]
	if filters.get("journal_entry"):
		conditions += "and jv1.name = '%s'" % filters["journal_entry"]
	if filters.get("entry_type") == "Write Off Entry":
		conditions += "and jv1.voucher_type = 'Write Off Entry'"
	elif filters.get("entry_type") == "Journal Entry":
		conditions += "and jv1.voucher_type = 'Journal Entry'"
	elif filters.get("entry_type") == "Cash Entry":
		conditions += "and jv1.voucher_type = 'Cash Entry'"
	elif filters.get("entry_type") == "Bank Entry":
		conditions += "and jv1.voucher_type = 'Bank Entry'"
	elif filters.get("entry_type") == "Debit Note":
		conditions += "and jv1.voucher_type = 'Debit Note'"
	elif filters.get("entry_type") == "Credit Note":
		conditions += "and jv1.voucher_type = 'Credit Note'"
	else:
		conditions += ""

	return conditions
