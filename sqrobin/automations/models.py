from django.db import models
import json
import uuid
from sqrobin import config
from profiles.models import Distributor
import requests
import sendgrid

"""
An Automation is a "template" for an Action. It describes how incoming data (about email
	recipients, POST-endpoints, etc.) should be formatted and distributed. When an Automation
	is invoked along with the appropriate data, the automated thing (email or POST) happens
	and an Action is created. The Action notes what Automation was invoked, and what the 
	result of that invocation was (status code, etc.).

	Many data items here begin their life as a python dictionary, get stuffed into json.dumps()
	and are saved as the resulting string. These strings can be decoded with json.loads() and
	used as dictionaries once again. For brevity, these are referred to as json dicts in the 
	comments below.
"""

class EmailAutomation(models.Model):
	#This UUID is supplied by the user when a new Lead is created. When that Lead is saved,
	#the custom save() looks up the appropriate automations by their invocation_key, creates
	#a MTM relationship to those automations, and fires the automation itself. 
	invocation_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	distributor = models.ForeignKey(Distributor)

	#json dict of name:email pairs to receive this email
	#when processing, you should use django.core.validators.validate_email to check recipient inputs
	recipients = models.TextField()
	sender_email = models.EmailField()

	#In practice these fields will contain "merge variables" that need to be formatted on a lead-by-lead
	#basis when generating the email
	#For example, a subject may be something like "New Lead: INSERT::FIRSTNAME INSERT::LASTNAME"
	subject = models.TextField()
	body = models.TextField()

	#user-friendly label for the automation
	label = models.CharField(max_length=150)

	def run(self, lead, **kwargs):
		"""
		formats data for a given lead and sends emails according to the parameters set on the model
		returns status; does NOT create or update Action model

		construct a "merge dict" of variables used to format the text body like:
			"::FIRSTNAME::" : lead.first_name

		iterate over keys in merge dict, replace instances in email subject & body with values
		"""
		merge_dict = {
			"::FIRSTNAME::" : lead.first_name,
			"::LASTNAME::": lead.last_name,
			"::HOMEPHONE::": lead.home_phone,
			"::CELLPHONE::": lead.cell_phone,
			"::BUSINESSPHONE::": lead.business_phone,
			"::EMAIL::": lead.email,
			"::PERSONALADDRESS::": lead.personal_address,
			"::PERSONALADDRESS2::": lead.personal_address_2,
			"::PERSONALCITY::": lead.personal_city,
			"::PERSONALSTATE::": lead.personal_state,
			"::PERSONALZIP::": lead.personal_zip,
			"::BUSINESSADDRESS::": lead.business_address,
			"::BUSINESSADDRESS2::": lead.business_address_2,
			"::BUSINESSCITY::": lead.business_city,
			"::BUSINESSSTATE::": lead.business_state,
			"::BUSINESSZIP::": lead.business_zip,
			"::FAXNUMBER::": lead.fax_number,
			"::INDUSTRY::": lead.industry,
			"::POSITION::": lead.position,
			"::WEBSITE::": lead.website,
			"::DOB::": lead.dob,
			"::COMMENTS::": lead.comments,
			"::REFERRAL::": lead.referral,
			"::NOTES::": lead.notes,
			"::CREATEDON::": str(lead.created_on) 
		}
		#format both body and subject; don't work directly on self.body/self.subject
		formatted_body = self.body
		formatted_subject = self.subject
		for key, value in merge_dict.items():
			if key in formatted_body:
				formatted_body = formatted_body.replace(key, value)
			if key in formatted_subject:
				formatted_subject = formatted_subject.replace(key, value)


		#create sendgrid message object & auth thing
		key = config.sg_key
		sg = sendgrid.SendGridClient(key)
		message = sendgrid.Mail()
		
		#format recipients and add to message
		recipients = self.recipients_to_dict()
		for name, email in recipients.items():
			r = "{} <{}>".format(name, email)
			message.add_to(r)

		message.set_subject(formatted_subject)
		message.set_text(formatted_body) #plain text emails only for now
		message.set_from(self.sender_email)

		status, msg = sg.send(message)
		#return something that can be used as the "status" attribue of the associated action
		print status, msg
		if status == 200:
			return "<Success: Email Created & Sent>"
		else:
			return "<Error: Undefined Error (status: {})>".format(status)

	def recipients_to_dict(self):
		return json.loads(self.recipients)

	def recipients_to_form_friendly_string(self):
		"""
		When rendering a ModelForm with an instance, we can't just render the stored json dict - 
		it would fail form validation. We need to construct an appropriate string that can be 
		used as the form's initial value.

		we split at \r\n because that's the way the data comes in from a given ModelForm
		"""
		recipient_dict = json.loads(self.recipients)
		constructor = ""
		for key, value in recipient_dict.items():
			constructor += "{}::{}\r\n".format(key, value) #Name::Email + newline
		return constructor

	def __unicode__(self):
		return self.label


class PostAutomation(models.Model):
	invocation_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	distributor = models.ForeignKey(Distributor)

	endpoint = models.URLField()

	#json dict of local data to send and what name to send it under (ie., data stored on the lead field)
	#For instance, the pair first_name:fname would mean "for any given"
	#lead, send its "first_name" value under the label "fname"
	lead_data = models.TextField()

	#json dict of custom data to send, stored like Label:Value (example: 'affiliateID': '123')
	custom_data = models.TextField()

	label = models.CharField(max_length=150)

	def run(self, lead, **kwargs):
		#Formats data for a given lead and fires according to the parameters set on the model
		#returns status; does NOT create or update Action model

		data = {}
		#Construct lead data to send
		for local_name, sending_label in json.loads(self.lead_data).items():
			data[sending_label] = getattr(lead, local_name)

		#Construct custom data to send
		for label, value in json.loads(self.custom_data).items():
			data[label] = value

		return requests.post(self.endpoint, data=data)



	def lead_data_to_dict(self):
		return json.loads(self.lead_data)

	def custom_data_to_dict(self):
		return json.loads(self.custom_data)

	def lead_data_to_form_friendly_string(self):
		"""
		When rendering a ModelForm with an instance, we can't just render the stored json dict - 
		it would fail form validation. We need to construct an appropriate string that can be 
		used as the form's initial value.

		we split at \r\n because that's the way the data comes in from a given ModelForm
		"""
		lead_data_dict = json.loads(self.lead_data)
		constructor = ""
		for key, value in lead_data_dict.items():
			constructor += "{}::{}\r\n".format(key, value) #LocalName::ForeignName + newline
		return constructor

	def custom_data_to_form_friendly_string(self):
		"""
		When rendering a ModelForm with an instance, we can't just render the stored json dict - 
		it would fail form validation. We need to construct an appropriate string that can be 
		used as the form's initial value.

		we split at \r\n because that's the way the data comes in from a given ModelForm
		"""
		custom_data_dict = json.loads(self.custom_data)
		constructor = ""
		for key, value in custom_data_dict.items():
			constructor += "{}::{}\r\n".format(key, value) #Label::Value + newline
		return constructor

	def __unicode__(self):
		return self.label


class EmailAction(models.Model):
	automation = models.ForeignKey(EmailAutomation)
	lead = models.ForeignKey('leads.Lead')
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	#Automations are run via m2m_changed signal on the lead. 
	#The receivier for that signal creates an Action with a pending status, runs the action, then updates
	#the status field with the result
	status = models.TextField()

	class Meta:
		unique_together = ('automation', 'lead')

	def __unicode__(self):
		return "{} for {} {}: {}".format(self.automation.label, self.lead.first_name, self.lead.last_name, self.status)

class PostAction(models.Model):
	automation = models.ForeignKey(PostAutomation)
	lead = models.ForeignKey('leads.Lead')
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	#After a lead is saved, the m2m_changed signal's receiver creates an action with 'pending' status, 
	#runs the action, then updates the status accordingly
	status = models.TextField()

	class Meta:
		unique_together = ('automation', 'lead')

	def __unicode__(self):
		return "{} for {} {}: {}".format(self.automation.label, self.lead.first_name, self.lead.last_name, self.status)