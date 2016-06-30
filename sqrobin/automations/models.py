from django.db import models
import json
import uuid
from profiles.models import Distributor

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
		#formats data for a given lead and sends emails according to the parameters set on the model
		#returns status; does NOT create or update Action model
		print "Running EmailAutomation %s for %r" % (self.invocation_key, lead)
		return "<Status: Queued>"

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
	#Stored like LocalName:ForeignName. For instance, the pair first_name:fname would mean "for any given"
	#lead, send its "first_name" value under the label "fname"
	lead_data = models.TextField()

	#json dict of custom data to send, stored like Label:Value (example: 'affiliateID': '123')
	custom_data = models.TextField()

	label = models.CharField(max_length=150)

	def run(self, lead, **kwargs):
		#Formats data for a given lead and fires according to the parameters set on the model
		#returns status; does NOT create or update Action model
		print "Running PostAutomation %s for %r" % (self.invocation_key, lead)
		return "<Status:201>"

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
		return self.automation.label, self.status

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
		return self.automation.label, self.status