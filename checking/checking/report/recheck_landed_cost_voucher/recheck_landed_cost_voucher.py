# Copyright (c) 2013, molie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _, scrub

def execute(filters=None):
	if not filters: filters = frappe._dict()
	validate_filters(filters)
	lcv_data = LcvGenerator(filters)
	data = []
	source = lcv_data.grouped_data if filters.get("group_by") != "Purchase Receipt" else lcv_data.data
	group_wise_columns = frappe._dict({
		"no.lcv": ["parent","posting_date","total_amountxd"],
		"purchase_receipt": ["parent", "purchase_receipt","supplier","posting_date","total_amountxd","total_amountxd1"],
		"receipt_document": ["parent", "receipt_document","supplier","posting_date","total_amountxd","total_amountxd1"],
		"item_code": ["parent","item_code","supplier","posting_date","total_amountxd","total_amountxd1"]
	})

	columns = get_columns(group_wise_columns, filters)
	for src in source:
		row = []
		for col in group_wise_columns.get(scrub(filters.group_by)):
			row.append(src.get(col))
		data.append(row)
	return columns, data

def get_columns(group_wise_columns, filters):
	columns = []
	column_map = frappe._dict({
		"parent": _("No. LCV")+":Link/Landed Cost Voucher:80",
		"purchase_receipt": _("Old No. Purchase Receipt")+":Link/Purchase Receipt:180",
		"receipt_document": _("No. Purchase Receipt")+":Link/Purchase Receipt:150",
		"item_code": _("Item Name") + ":Link/Item:300",
		"supplier": _("Supplier Name") + ":Link/Supplier:300",
		"posting_date": _("Posting Date") + ":Date:100",
		"total_amountxd": _("Amount /ITEM") + ":Currency:120",
		"total_amountxd1": _("Amount /ITEM1") + ":Currency:120"
	})

	for col in group_wise_columns.get(scrub(filters.group_by)):
		columns.append(column_map.get(col))
	return columns

def validate_filters(filters):
	if (filters.get("group_by") == "no.lcv" and filters.get("landed_cost_voucher") is None ):
		frappe.throw(_("please, fill landed cost voucher number if you use filter by no.lcv "))

	if (filters.get("group_by") == "Purchase Receipt" and filters.get("purchase_receipt") is not None):
		frappe.throw(_("please, don't fill purchase receipt number if you use filter by Purchase Receipt \
		 and don't use sort order by Purchase Receipt in table. Bugs! "))

def get_recheck_landed_cost_voucher(filters):
		conditions = get_conditions(filters)
		return frappe.db.sql(
			"""select
					lcv3.parent,
					lcv3.purchase_receipt,
					lcv3.receipt_document,
					pr1.supplier,
					pr1.posting_date,
					sum(if(lcv3.item_code,lcv3.applicable_charges,0)) as total_amountxd,
					sum(lcv3.applicable_charges) as total_amountxd1,
					lcv3.creation,lcv3.owner,
					lcv3.modified,lcv3.modified_by
			   from
			   		`tabLanded Cost Item` lcv3
					inner join `tabPurchase Receipt` pr1
			   where
			   		((pr1.name = lcv3.purchase_receipt) or (pr1.name = lcv3.receipt_document))
					and lcv3.docstatus < 2 %s
			""" % conditions, as_list=1)

class LcvGenerator(object):
	def __init__(self, filters=None):
		self.data = []
		self.filters = frappe._dict(filters)
		self.load_invoice_items()
		self.process()

	def process(self):
		self.grouped = {}
		for row in self.si_list:
			# add to grouped
			if self.filters.group_by != "Purchase Receipt":
				self.grouped.setdefault(row.get(scrub(self.filters.group_by)), []).append(row)
			self.data.append(row)

		if self.grouped:
			self.collapse_group()
		else:
			self.grouped_data = []

	def collapse_group(self):
		# sum buying / selling totals for group
		self.grouped_data = []
		for key in self.grouped.keys():
			for i, row in enumerate(self.grouped[key]):
				if i==0:
					new_row = row
			self.grouped_data.append(new_row)

	def load_invoice_items(self):
		conditions = ""
		if self.filters.landed_cost_voucher:
			conditions += " and lcv3.parent = %(landed_cost_voucher)s"
		if self.filters.purchase_receipt:
			conditions += " and lcv3.purchase_receipt = %(purchase_receipt)s"
		if self.filters.supplier:
			conditions += " and pr1.supplier = %(supplier)s"
		if self.filters.from_date:
			conditions += " and pr1.posting_date >= %(from_date)s"
		if self.filters.to_date:
			conditions += " and pr1.posting_date <= %(to_date)s"

		if self.filters.group_by == "Purchase Receipt":
			conditions +="and lcv3.purchase_receipt != '' group by lcv3.purchase_receipt order by lcv3.purchase_receipt desc,pr1.posting_date desc"
		elif self.filters.group_by == "Item Code":
				conditions +="group by lcv3.item_code, lcv3.parent order by pr1.posting_date desc"
		elif self.filters.group_by == "Receipt Document":
					conditions +="and lcv3.receipt_document != '' group by lcv3.receipt_document order by lcv3.receipt_document desc,pr1.posting_date desc"
		else:
				conditions +="order by lcv3.purchase_receipt desc,pr1.posting_date desc"

		self.si_list = frappe.db.sql("""select
				lcv3.parent,
				lcv3.purchase_receipt,
				lcv3.receipt_document,
				lcv3.item_code,
				pr1.supplier,
				pr1.posting_date,
				sum(if(lcv3.item_code,lcv3.applicable_charges,0)) as total_amountxd,
				sum(lcv3.applicable_charges) as total_amountxd1,
				lcv3.creation,lcv3.owner,
				lcv3.modified,lcv3.modified_by
		   from
				`tabLanded Cost Item` lcv3
				inner join `tabPurchase Receipt` pr1

		   where
				((pr1.name = lcv3.purchase_receipt) or (pr1.name = lcv3.receipt_document))
				and lcv3.docstatus < 2 %s

			""" % (conditions,), self.filters, as_dict=1)
