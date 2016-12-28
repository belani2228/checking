# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr
from frappe import _
import frappe.defaults
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate, add_days

from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.utils import get_account_currency
from frappe.desk.notifications import clear_doctype_notifications


def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_purchase_receipt(filters)

	return columns, data

def get_columns():
	return [
	    _("Status") + ":Data:80",
		_("Document") + "::120",
		_("No.Purchase Receipt")+":Link/Purchase Receipt:150",
		_("No.Pu")+":Data:120",
		_("No.BL")+":Data:140",
		_("Supplier Name") + ":Link/Supplier:300",
		_("PostingDate") + ":Date:100",
		_("PostingTime") + ":Time:100",
		_("No.Document") + ":Data:120",
		_("VehicleDate") + ":Date:100",
		_("No.Vehicle") + ":Data:100",
		_("Currency") + ":Data:100",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount") + ":Currency/Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Amount (IDR) Rounded") + ":Currency:150",
		_("CreatedDate") + ":Datetime:150",
		_("CreatedBy") + ":Data:200",
		_("ModifiedDate") + ":Datetime:150",
		_("ModifiedBy") + ":Data:200"
	]

def get_recheck_purchase_receipt(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select
				status,
				if(is_return = 1,"Return","Purchase Receipt"),
				name,
				pu_number,
				bl_no,
				supplier,
				posting_date,
				posting_time,
				transporter_name,
				lr_date,
				lr_no,
				currency,
				conversion_rate,
				net_total,
				base_total,
				base_rounded_total,
				creation,
				owner,
				modified,
				modified_by
		   from
		   		`tabPurchase Receipt`
		   where
		   		docstatus < 2 %s order by name desc,posting_date desc,posting_time desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""

	if filters.get("from_date"):
		conditions += "and posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and posting_date <= '%s'" % filters["to_date"]

	if filters.get("purchase_receipt"):
		conditions += "and name = '%s'" % filters["purchase_receipt"]

	if filters.get("recheck_month") == "If Posting Date > Created Date":
		conditions += "and (date(posting_date) > date(creation))"
	elif filters.get("recheck_month") == "If Posting Date < Created Date":
		conditions += "and (date(posting_date) < date(creation))"
	elif filters.get("recheck_month") == "If Posting Date > Vehicle Date":
		conditions += "and (date(posting_date) > date(lr_date))"
	elif filters.get("recheck_month") == "If Posting Date < Vehicle Date":
		conditions += "and (date(posting_date) < date(lr_date))"
	elif filters.get("recheck_month") == "Posting Date (Year) > Vehicle Date (Year)":
		if filters.get("from_date") is not None or filters.get("to_date") is not None:
			frappe.throw(_("please, don't fill from date  and to date"))

		conditions += "and (year(posting_date) > year(lr_date))"
	elif filters.get("recheck_month") == "Posting Date (Year) > Created Date (Year)":
		if filters.get("from_date") is not None or filters.get("to_date") is not None:
			frappe.throw(_("please, don't fill from date  and to date"))

		conditions += "and (year(posting_date) > year(creation))"

	else:
		conditions += ""

	if filters.get("entry_type") == "Draft":
		conditions += "and docstatus = '0' and is_return = '0'"
	elif filters.get("entry_type") == "To Bill":
		conditions += "and docstatus = '1' and is_return = '0' and per_billed < '100'"
	elif filters.get("entry_type") == "Completed":
		conditions += "and docstatus = '1' and is_return = '0' and per_billed = '100'"
	elif filters.get("entry_type") == "Return":
		conditions += "and is_return = '1'"
	else:
		conditions += "and per_billed <= '100'"
	return conditions
