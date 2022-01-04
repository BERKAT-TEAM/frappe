frappe.listview_settings['Contact'] =  {
	add_fields: ["image"],
	filters: [["owner", "=", frappe.session.user]],
};