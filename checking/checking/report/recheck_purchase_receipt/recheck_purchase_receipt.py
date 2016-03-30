# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr
from frappe import _
import frappe.defaults

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
		_("No.Purchase Receipt")+":Link/Purchase Receipt:150",
		_("Supplier Name") + ":Link/Supplier:300",
		_("Posting Date") + ":Date:100",
		_("Posting Time") + ":Time:100",
		_("No.Document") + ":Data:120",
		_("Document Date") + ":Date:100",
		_("No.Vehicle") + ":Data:100",
		_("Currency") + ":Link/Currency:100",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount") + ":Currency/Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Amount (IDR) Rounded") + ":Currency:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]


def get_recheck_purchase_receipt(filters):
	conditions = get_conditions(filters)
	#return frappe.db.sql("""select item_name,item_group,stock_uom,expense_account,income_account,has_variants,is_purchase_item,is_sales_item,is_asset_item,is_sub_contracted_item from tabItem where has_variants = '0' and item_group = 'layanan' %s""" % conditions, as_list=1)
	return frappe.db.sql(
		"""select
				status,name,supplier,posting_date,posting_time,transporter_name,lr_date,lr_no,
				currency,conversion_rate,net_total,base_total,base_rounded_total,creation,owner,
				modified,modified_by
		   from
		   		`tabPurchase Receipt`
		   where
		   		docstatus < 2 %s order by name desc,posting_date desc,posting_time desc
		""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("from_date"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):

		#conditions += "and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
		conditions += "and posting_date <= '%s'" % filters["to_date"]

	if filters.get("purchase_receipt"):
		conditions += "and name = '%s'" % filters["purchase_receipt"]

	return conditions
