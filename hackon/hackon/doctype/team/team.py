# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import *
from frappe.model.document import Document

class Team(Document):
	pass

@frappe.whitelist()
def create_project_custom_button(source_name, target_doc = None):
	doc = get_mapped_doc(
        'Team',
        source_name,
        {
        'Team': {
        'doctype': 'Project',
        }
        })
	return doc