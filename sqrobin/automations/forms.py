from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
import json
from automations.models import EmailAutomation, PostAutomation, EmailAction, PostAction


class EmailAutomationForm(forms.ModelForm):
	class Meta:
		model = EmailAutomation
		#note: recipients will require custom validation and processing
		#use django.core.validators.validate_email etc., create json dict
		fields = ('recipients', 'sender_email', 'subject', 'body', 'label')

	def clean_recipients(self):
		clean_data = self.cleaned_data['recipients']
		processed_data = {}
		"""
		Recipients come in like so:

		Name::Email
		Name::Email

		First, split on newlines and remove blank lines. Then split each line on :: and validate email
		for the right-hand side. Then, stuff things into the processed_data dict. Then, json.dumps and return
		"""
		newline_split = [line for line in clean_data.split('\r\n') if line]
		for pair in newline_split:
			split_pair = pair.split("::")
			try:
				validators.validate_email(split_pair[1])
				#convert data to dictionary: {name: email, name:email}
				processed_data[split_pair[0]] = split_pair[1]
			except ValidationError:
				raise forms.ValidationError("Invalid email recipient detected: %(value)s",
											code='invalid',
											params={'value':split_pair[1]},
											)
		#return json dump of processed_data; should save stringified dict? //TODO: Test
		return json.dumps(processed_data)



class PostAutomationForm(forms.ModelForm):
	class Meta:
		model = PostAutomation
		#lead_data & custom_data will need custom validation and processing (json dicts)
		fields = ('label', 'endpoint', 'lead_data', 'custom_data')

	def clean_lead_data(self):
		"""
		lead_data validators check to make sure the specified local names exist & that every local
		name is paired with an external label under which to send it.

		this data comes in like so:

		LocalName::ExternalLabel
		LocalName::ExternalLabel

		First, split on newlines and remove blank lines. Then split each line at :: and make sure each 
		resulting list has len==2. Then, check that the first item in the list is a valid local name.

		If all is good, reformat into a dict and store as a json dump
		"""
		clean_data = self.cleaned_data['lead_data']
		processed_data = {}

		valid_local_names = [
							'first_name',
							'last_name',
							'home_phone',
							'cell_phone',
							'business_phone',
							'email',
							'personal_address',
							'personal_address_2',
							'personal_city',
							'personal_state',
							'personal_zip',
							'business_address',
							'business_address_2',
							'business_city',
							'business_state',
							'business_zip',
							'fax_number',
							'industry',
							'position',
							'website',
							'dob',
							'comments',
							'referral',
							'notes'
							]	
		newline_split = [line for line in clean_data.split('\r\n') if line]
		for pair in newline_split:
			split_pair = pair.split("::")
			if len(split_pair) != 2:
				raise forms.ValidationError("Mismatch at %(value)s: local name must have exactly one external label",
											code='invalid',
											params={'value':split_pair[0]},
											)
			elif split_pair[0] not in valid_local_names:
				raise forms.ValidationError("Invalid local name: %(value)s",
											code='invalid',
											params={'value':split_pair[0]},
											)
			else:
				processed_data[split_pair[0]] = split_pair[1]

		return json.dumps(processed_data)


	def clean_custom_data(self):
		"""
		Custom data comes in like so:

		Label::Value
		Label::Value

		Split on newlines & remove blanks, make sure each label has exactly one value, save as json dump
		"""
		clean_data = self.cleaned_data['custom_data']
		processed_data = {}

		newline_split = [line for line in clean_data.split('\r\n') if line]
		for pair in newline_split:
			split_pair = pair.split("::")
			if len(split_pair) != 2:
				raise forms.ValidationError("Mismatch at %(value)s: labels must have exactly one value",
											code='invalid',
											params={'value':split_pair[0]},
											)
			else:
				processed_data[split_pair[0]] = split_pair[1]

		return json.dumps(processed_data)







































