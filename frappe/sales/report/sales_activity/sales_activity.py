# Copyright (c) 2013, Ming Promotion and contributors
# License: MIT. See LICENSE

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
# from erpnext.crm.report.campaign_efficiency.campaign_efficiency import get_activity

def execute(filters=None):
	columns, data = [], []
	filters = frappe._dict(filters or {})
	
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))
	
	columns = get_columns(filters)
	data = get_data(filters)

	# chart_data = get_chart_data(data)

	return columns, data

def get_columns(filters):
	return [
		{
			"fieldname": "user",
			"label": _("Sales Name"),
			"fieldtype": "Link",
			"options": "User",
			"width": "200"
		},
		{
			"fieldname": "email_count",
			"label": _("Count Email"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "sales_call_count",
			"label": _("Count Sales Call"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "vising_count",
			"label": _("Count Kanvasing/Visit"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "survey_count",
			"label": _("Count Survey"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "meet_count",
			"label": _("Count Meeting"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "entertain_count",
			"label": _("Count Entertain"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "total",
			"label": _("Total Activity"),
			"fieldtype": "Float",
			"width": "150"
		}

	]

def get_data(filters):
	data = []

	# company_list = get_descendants_of("Company", filters.get("company"))
	quo_records = get_quotation_details(filters)
	for record in quo_records:
		row = {
			"user": record[0],
			"email_count": record[1],
			"sales_call_count": record[2],
			"vising_count": record[3],
			"survey_count": record[4],
			"meet_count": record[5],
			"entertain_count": record[6],
			"total": record[7]
		}
		data.append(row)
	return data

def get_quotation_details(filters):
	
	query = frappe.db.sql("""
		SELECT 
			sales_person as Sales, 
			COUNT(CASE WHEN activity = "- Email" THEN 0 END) as "Count Email",
			COUNT(CASE WHEN activity = "- Sales Call" THEN 0 END) as "Count Sales Call",
			COUNT(CASE WHEN activity = "- Kanvasing/Visit" THEN 0 END) as "Count Kanvasing/Visit",
			COUNT(CASE WHEN activity = "- Survey" THEN 0 END) as "Count Survey",
			COUNT(CASE WHEN activity = "- Meeting" THEN 0 END) as "Count Meeting",
			COUNT(CASE WHEN activity = "- Entertain" THEN 0 END) as "Count Entertain",
			COUNT(activity) as "Total Activity"
		FROM `tabSales Activity` 
		WHERE date(creation) >= %(s)s AND date(creation) <= %(t)s
		GROUP BY sales_person
		ORDER BY COUNT(activity) DESC;
	""", {
		"s": filters.from_date,
		"t": filters.to_date
	})
	print(query)

	return query

# def get_chart_data(data):
# 	item_wise_quo_map = {}
# 	labels, datapoints = [], []

# 	for row in data:
# 		item_key = row.get("item_name")

# 		if not item_key in item_wise_quo_map:
# 			item_wise_quo_map[item_key] = 0

# 		item_wise_quo_map[item_key] = flt(item_wise_quo_map[item_key]) + flt(row.get("amount"))

# 	item_wise_quo_map = { 
# 		item: value for item, 
# 		value in (
# 			sorted(item_wise_quo_map.items(), 
# 			key = lambda i: i[1], 
# 			reverse=True
# 			)
# 		)
# 	}

# 	for key in item_wise_quo_map:
# 		labels.append(key)
# 		datapoints.append(item_wise_quo_map[key])

# 	return {
# 		"data" : {
# 			"labels" : labels[:30], # show max of 30 items in chart
# 			"datasets" : [
# 				{
# 					"name" : _(" Total Sales Amount"),
# 					"values" : datapoints[:30]
# 				}
# 			]
# 		},
# 		"type" : "bar"
# 	}