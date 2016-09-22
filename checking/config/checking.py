from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Report"),
			"items": [
				{
					"type": "doctype",
					"name": "Report Center",
					"description": _("Report Center - Beta")
				},
				{
					"type": "report",
					"name": "Ending Stock",
					"is_query_report": True,
					"doctype": "Report Center"
				},
				{
					"type": "report",
					"name": "Stock Card",
					"is_query_report": True,
					"doctype": "Report Center"
				}
			]

		},
		{
			"label": _("List"),
			"items": [
				{
					"type": "report",
					"name": "List Item Product",
					"is_query_report": True,
					"doctype": "Report Center"
				},
				{
					"type": "report",
					"name": "List Item Service",
					"is_query_report": True,
					"doctype": "Report Center"
				},
				{
					"type": "report",
					"name": "List Item Assets",
					"is_query_report": True,
					"doctype": "Report Center"
				},
				#{
				#	"type": "report",
				#	"name": "Chart of Account",
				#	"doctype": "Report Center",
				#	"is_query_report": True,
				#}

			]
		},
		{
			"label": _("Tracking Error"),
			"icon": "icon-table",
			"items": [
				{
					"type": "report",
					"name": "Check Error Purchase Receipt Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Check Error Landed Cost Voucher",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Check Error Purchase Invoice Landed Cost",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Check Error Delivery Note Item",
					"doctype": "Report Center",
					"is_query_report": True,
				}
			]
		},
		{
			"label": _("Recheck Purchase"),
			"icon": "icon-flag",
			"items": [
				{
					"type": "report",
					"name": "Recheck Purchase Receipt",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Purchase Receipt Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Purchase Invoice",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Purchase Invoice Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Purchase Invoice LCV",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Purchase Invoice LCV Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Recheck Landed Cost"),
			"icon": "icon-table",
			"items": [
				{
					"type": "report",
					"name": "Recheck Landed Cost Voucher",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Landed Cost Voucher Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Recheck Sales"),
			"icon": "icon-table",
			"items": [
				{
					"type": "report",
					"name": "Recheck Delivery Note",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Delivery Note Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Sales Invoice",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Sales Invoice Item",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Item Never Been Sold",
					"doctype": "Report Center",
					"is_query_report": True,
				}
			]
		},
		{
			"label": _("Recheck COGS"),
			"icon": "icon-table",
			"items": [
				{
					"type": "report",
					"name": "Recheck COGS",
					"doctype": "Report Center",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Recheck Journal"),
			"icon": "icon-table",
			"items": [
				{
					"type": "report",
					"name": "Recheck Journal Entry",
					"doctype": "Report Center",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Recheck Journal Entry Detail",
					"doctype": "Report Center",
					"is_query_report": True,
				},
			]
		},

	]
