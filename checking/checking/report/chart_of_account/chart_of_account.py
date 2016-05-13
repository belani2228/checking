# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate, cstr
from erpnext.accounts.report.financial_statements \
	import filter_accounts, set_gl_entries_by_account, filter_out_zero_value_rows

value_fields = ("opening_debit","closing_debit")

def execute(filters=None):
	data = get_data(filters)
	columns = get_columns()
	return columns, data


def get_data(filters):
	accounts = frappe.db.sql("""select name, parent_account, account_name, root_type, report_type, lft, rgt
		from `tabAccount` where company=%s order by lft""", filters.company, as_dict=True)

	if not accounts:
		return None

	accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)
	gl_entries_by_account = {}
	opening_balances = get_opening_balances(filters)

	total_row = calculate_values(accounts, gl_entries_by_account, opening_balances)
	accumulate_values_into_parents(accounts, accounts_by_name)

	data = prepare_data(accounts,parent_children_map)
	data = filter_out_zero_value_rows(data, parent_children_map,
		show_zero_values=filters.get("show_zero_values"))

	return data

#-------------------------------------------------------------------------------------------
def get_opening_balances(filters):
	balance_sheet_opening = get_rootwise_opening_balances(filters, "Balance Sheet")
	pl_opening = get_rootwise_opening_balances(filters, "Profit and Loss")
	balance_sheet_opening.update(pl_opening)
	return balance_sheet_opening

def get_rootwise_opening_balances(filters, report_type):
	additional_conditions = ""

	gle = frappe.db.sql("""
		select
			account, sum(debit) as opening_debit
		from `tabGL Entry`
		where
			company=%(company)s
			{additional_conditions}
			and account in (select name from `tabAccount`)
		group by account""".format(additional_conditions=additional_conditions),
		{
			"company": filters.company
		},
		as_dict=True)

	opening = frappe._dict()
	for d in gle:
		opening.setdefault(d.account, d)

	return opening

def calculate_values(accounts, gl_entries_by_account, opening_balances):
	init = {
		"opening_debit": 0.0,
		"closing_debit": 0.0
		
	}

	for d in accounts:
		d.update(init.copy())

		# add opening
		d["opening_debit"] = opening_balances.get(d.name, {}).get("opening_debit", 0)


def accumulate_values_into_parents(accounts, accounts_by_name):
	for d in reversed(accounts):
		if d.parent_account:
			for key in value_fields:
				accounts_by_name[d.parent_account][key] += d[key]

def prepare_data(accounts,parent_children_map):
	data = []


	for d in accounts:
		has_value = False
		row = {
			"account_name": d.account_name,
			"account": d.name,
			"parent_account": d.parent_account,
			"indent": d.indent,
		}


		for key in value_fields:
			row[key] = flt(d.get(key, 0.0), 3)

			if abs(row[key]) >= 0.005:
				# ignore zero values
				has_value = True

		row["has_value"] = has_value
		data.append(row)

	return data

def get_columns():
	return [
		{
			"fieldname": "account",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 1080
		}
	]
