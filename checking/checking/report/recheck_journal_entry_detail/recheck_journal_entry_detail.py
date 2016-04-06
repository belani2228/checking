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
	data = get_recheck_journal_entry_detail(filters)
	return columns, data

def get_columns():
	return [
	    _("Status") + "::80",
		_("VoucherType") + "::100",
		_("No.Journal Entry")+":Link/Journal Entry:150",
		_("Posting Date") + ":Date:100",
		_("Account") + "::300",
		_("Debit (IDR & Other)") + ":Float:120",
		_("Credit (IDR & Other)") + ":Float:120",
		_("Rate (IDR to Other)") + ":Currency/Float:120",
		_("Total Debit (IDR)") + ":Float:120",
		_("Total Credit (IDR)") + ":Float:120",
		_("Cost Center")+":Link/Cost Center:150",
		_("Account Type") + "::300",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_journal_entry_detail(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				if(jv1.docstatus = '1',"Submit","Draft") as docstatusjv,
				jv1.voucher_type,
				jv2.parent,
				jv1.posting_date,
				jv2.account,
				jv2.debit_in_account_currency,
				jv2.credit_in_account_currency,
				jv2.exchange_rate,
				jv2.debit,
				jv2.credit,
				jv2.cost_center,
				jv2.account_type,
				jv2.creation,jv2.owner,
				jv2.modified,jv2.modified_by
		   from
		   		`tabJournal Entry` jv1
				inner join `tabJournal Entry Account` jv2
		   where
		   		jv1.name = jv2.parent
		   		and jv1.docstatus < 2 %s
		   order by
		   		jv1.name desc, jv1.posting_date desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("account"):
		conditions += "and jv2.account = '%s'" % filters["account"]
	if filters.get("cost_center"):
		conditions += "and jv2.cost_center = '%s'" % filters["cost_center"]
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

	if filters.get("entry_document") == "Draft":
		conditions += "and jv1.docstatus = '0'"
	elif filters.get("entry_document") == "Submit":
		conditions += "and jv1.docstatus = '1'"
	else:
		conditions += ""

	return conditions
