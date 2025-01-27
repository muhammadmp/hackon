# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import *
from frappe.model.document import Document

class Team(Document):
	def after_insert(self):
		if frappe.session.user == self.owner:
			if frappe.db.exists('Participant', {'user' : frappe.session.user}):
				participant_doc = frappe.get_doc('Participant', {'user' : frappe.session.user})
				participant_doc.team_lead = 1
				participant_doc.save()

	def validate(self):
		self.total_active_members = len(self.participants)
		score = 0.0
		for participant in self.participants:
			if participant.participant_score:
				score += participant.participant_score
		if score:
			self.team_score = float(score)

@frappe.whitelist()
def change_team_lead(new_team_lead, name):
	if frappe.db.exists('Team', name):
		doc_name = frappe.get_doc('Team',name)
		doc_name.team_lead = new_team_lead
		doc_name.save()
		if doc_name.team_lead:
			frappe.db.set_value('Participant',doc_name.team_lead,'team_lead',0)
			doc_name.team_lead = new_team_lead
			frappe.db.set_value('Participant',new_team_lead,'team_lead',1)
			doc_name.save()
		return True

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

@frappe.whitelist()
def mentor_user_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT
            u.name
        FROM
            `tabUser` u ,
            `tabHas Role` r
        WHERE
            u.name = r.parent and
            u.name != 'Administrator' and
            r.role = 'Mentor' and
            u.enabled = 1 and
            u.name like %s
    """, ("%" + txt + "%"))
