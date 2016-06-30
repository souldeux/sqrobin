from django import forms
from leads.models import Lead

class LeadForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = (
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
				'notes',
				'invoked_email_automations',
				'invoked_post_automations',
			)