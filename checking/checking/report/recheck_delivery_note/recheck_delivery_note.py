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
	    _("Status") + ":Data:80",
		_("No.Delivery Note")+":Link/Delivery Note:100",
		_("Customer Name") + ":Link/Customer:300",
		_("Customer Group") + ":Link/Customer Group:120",
		_("Territory") + ":Link/Territory:100",
		_("Posting Date") + ":Date:100",
		_("Posting Time") + ":Time:100",
		_("No.Document") + ":Data:120",
		_("Document Date") + ":Date:100",
		_("No.Vehicle") + ":Data:100",
		_("Currency") + ":Link/Currency:100",
		_("Rate (IDR to Other)") + ":Currency:120",
		_("Amount") + ":Currency:120",
		_("Amount (IDR)") + ":Currency:120",
		_("Amount (IDR) Rounded") + ":Currency:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]


def get_recheck_delivery_note(filters):
	conditions = get_conditions(filters)
	#return frappe.db.sql("""select item_name,item_group,stock_uom,expense_account,income_account,has_variants,is_purchase_item,is_sales_item,is_asset_item,is_sub_contracted_item from tabItem where has_variants = '0' and item_group = 'layanan' %s""" % conditions, as_list=1)
	return frappe.db.sql(

		"""select
				status,name,customer,customer_group,territory,posting_date,posting_time,
				transporter_name,lr_date,lr_no,currency,conversion_rate,net_total,
				base_total,base_rounded_total,creation,owner,
				modified,modified_by
		   from
		   		`tabDelivery Note`
		   where
		   		docstatus < 2 %s order by name desc,posting_date desc,posting_time desc
		""" % conditions, as_list=1)
	#return frappe.db.sql("""select `tabPurchase Receipt`.status,`tabPurchase Receipt`.name,`tabPurchase Receipt`.supplier,`tabPurchase Receipt`.company,`tabPurchase Receipt`.posting_date,`tabPurchase Receipt`.posting_time,`tabPurchase Receipt`.transporter_name,`tabPurchase Receipt`.lr_date,`tabPurchase Receipt`.lr_no,`tabPurchase Receipt`.currency,`tabPurchase Receipt`.price_list_currency,`tabPurchase Receipt`.conversion_rate,`tabPurchase Receipt`.base_net_total,concat(`tabCurrency`.symbol," ",`tabPurchase Receipt`.base_grand_total),`tabPurchase Receipt`.net_total,`tabPurchase Receipt`.base_total,`tabPurchase Receipt`.base_rounded_total from `tabPurchase Receipt` inner join `tabCurrency` on `tabPurchase Receipt`.currency = `tabCurrency`.name where `tabPurchase Receipt`.docstatus < 2 %s""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	#value = []
	if filters.get("delivery_note"):
		conditions += "and name = '%s'" % filters["delivery_note"]

	if filters.get("customer_group"):
		conditions += "and customer_group = '%s'" % filters["customer_group"]

	if filters.get("territory"):
		conditions += "and territory = '%s'" % filters["territory"]

	if filters.get("from_date"):
		#conditions += "and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
		conditions += "and posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):

		#conditions += "and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
		conditions += "and posting_date <= '%s'" % filters["to_date"]


	return conditions

		#if filters.get("company"): conditions += " and company = '%s'" % \
		#	filters["company"].replace("'", "\\'")
