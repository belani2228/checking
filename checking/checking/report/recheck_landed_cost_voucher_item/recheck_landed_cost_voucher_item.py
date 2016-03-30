# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_recheck_landed_cost_voucher_item(filters)

	return columns, data

def get_columns():
	return [
		_("Status")+":Data:80",
		_("No. LCV")+":Link/Landed Cost Voucher:80",
		_("No. Purchase Receipt")+":Link/Purchase Receipt:150",
		_("Supplier Name") + ":Link/Supplier:250",

		_("Item Code") + ":Link/Item:300",
		_("Based On") + "::80",
		_("Amount LCV / QTY (IDR)") + ":Currency:150",
		_("Created Date") + ":Datetime:150",
		_("Created By") + ":Data:200",
		_("Modified Date") + ":Datetime:150",
		_("Modified By") + ":Data:200"
	]

def get_recheck_landed_cost_voucher_item(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		"""select distinct
				if(lcv1.docstatus = 0,"Draft","Submit") as docstatuslcv,
				lcv1.name,
				lcv3.purchase_receipt,
				lcv2.supplier,
				lcv3.item_code,
				lcv1.distribute_charges_based_on,
				lcv3.applicable_charges,
				lcv3.creation,lcv3.owner,
				lcv3.modified,lcv3.modified_by
		   from
		   		`tabLanded Cost Voucher` lcv1
				inner join `tabLanded Cost Purchase Receipt` lcv2
				inner join `tabLanded Cost Item` lcv3

		   where
		   		lcv2.parent = lcv1.name
				and lcv3.parent = lcv2.parent
				and lcv1.docstatus < 2 %s
				order by lcv1.name desc, lcv3.purchase_receipt desc, lcv2.posting_date desc
		""" % conditions, as_list=1)
	#return frappe.db.sql("""select `tabPurchase Receipt`.status,`tabPurchase Receipt`.name,`tabPurchase Receipt`.supplier,`tabPurchase Receipt`.company,`tabPurchase Receipt`.posting_date,`tabPurchase Receipt`.posting_time,`tabPurchase Receipt`.transporter_name,`tabPurchase Receipt`.lr_date,`tabPurchase Receipt`.lr_no,`tabPurchase Receipt`.currency,`tabPurchase Receipt`.price_list_currency,`tabPurchase Receipt`.conversion_rate,`tabPurchase Receipt`.base_net_total,concat(`tabCurrency`.symbol," ",`tabPurchase Receipt`.base_grand_total),`tabPurchase Receipt`.net_total,`tabPurchase Receipt`.base_total,`tabPurchase Receipt`.base_rounded_total from `tabPurchase Receipt` inner join `tabCurrency` on `tabPurchase Receipt`.currency = `tabCurrency`.name where `tabPurchase Receipt`.docstatus < 2 %s""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""

	if filters.get("from_date"):
		conditions += "and lcv2.posting_date >= '%s'" % filters["from_date"]

	if filters.get("to_date"):
		conditions += "and lcv2.posting_date <= '%s'" % filters["to_date"]

	if filters.get("landed_cost_voucher"):
		conditions += "and lcv1.name = '%s'" % filters["landed_cost_voucher"]

	if filters.get("purchase_receipt"):
		conditions += "and lcv3.purchase_receipt = '%s'" % filters["purchase_receipt"]

	if filters.get("supplier"):
		conditions += "and lcv2.supplier = '%s'" % filters["supplier"]

	return conditions

		#if filters.get("company"): conditions += " and company = '%s'" % \
		#	filters["company"].replace("'", "\\'")
