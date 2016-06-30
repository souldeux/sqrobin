from __future__ import unicode_literals

from django.db import models
from profiles.models import Distributor
from automations.models import EmailAutomation, PostAutomation, EmailAction, PostAction
from django.dispatch import receiver
from django.db.models.signals import m2m_changed



class Lead(models.Model):
	STATE_CHOICES = (
		('AL', 'Alabama'),
		('AK', 'Alaska'),
		('AZ', 'Arizona'),
		('AR', 'Arkansas'),
		('CA', 'California'),
		('CO', 'Colorado'),
		('CT', 'Connecticut'),
		('DE', 'Delaware'),
		('FL', 'Florida'),
		('GA', 'Georgia'),
		('HI', 'Hawaii'),
		('ID', 'Idaho'),
		('IL', 'Illinois'),
		('IN', 'Indiana'),
		('IA', 'Iowa'),
		('KS', 'Kansas'),
		('KY', 'Kentucky'),
		('LA', 'Louisiana'),
		('ME', 'Maine'),
		('MD', 'Maryland'),
		('MA', 'Massachusetts'),
		('MI', 'Michigan'),
		('MN', 'Minnesota'),
		('MS', 'Mississippi'),
		('MO', 'Missouri'),
		('MT', 'Montana'),
		('NE', 'Nebraska'),
		('NV', 'Nevada'),
		('NH', 'New Hampshire'),
		('NJ', 'New Jersey'),
		('NM', 'New Mexico'),
		('NY', 'New York'),
		('NC', 'North Carolina'),
		('ND', 'North Dakota'),
		('OH', 'Ohio'),
		('OK', 'Oklahoma'),
		('OR', 'Oregon'),
		('PA', 'Pennsylvania'),
		('RI', 'Rhode Island'),
		('SC', 'South Carolina'),
		('SD', 'South Dakota'),
		('TN', 'Tennessee'),
		('TX', 'Texas'),
		('UT', 'Utah'),
		('VT', 'Vermont'),
		('VA', 'Virginia'),
		('WA', 'Washington'),
		('WV', 'West Virginia'),
		('WI', 'Wisconsin'),
		('WY', 'Wyoming'),
		)
	
	distributor = models.ForeignKey(Distributor)
	created_on = models.DateTimeField(auto_now_add=True)

	first_name = models.CharField(max_length=75, blank=True)
	last_name = models.CharField(max_length=75, blank=True)
	home_phone = models.CharField(max_length=25, blank=True)
	cell_phone = models.CharField(max_length=25, blank=True)
	business_phone = models.CharField(max_length=25, blank=True)
	email = models.EmailField(max_length=100, blank=True)
	personal_address = models.CharField(max_length=200, blank=True)
	personal_address_2 = models.CharField(max_length=200, blank=True)
	personal_city = models.CharField(max_length=200, blank=True)
	personal_state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
	personal_zip = models.CharField(max_length=200, blank=True)
	business_address = models.CharField(max_length=200, blank=True)
	business_address_2 = models.CharField(max_length=200, blank=True)
	business_city = models.CharField(max_length=200, blank=True)
	business_state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
	business_zip = models.CharField(max_length=200, blank=True)
	fax_number = models.CharField(max_length=25, blank=True)
	industry = models.CharField(max_length=100, blank=True)
	position = models.CharField(max_length=100, blank=True)
	website = models.URLField(max_length=200, blank=True)
	dob = models.DateField(blank=True, null=True)
	comments = models.TextField(blank=True)
	referral = models.CharField(max_length=200, blank=True)
	notes = models.TextField(blank=True)

	#MTM relationships describing what automations to invoke
	invoked_email_automations = models.ManyToManyField(EmailAutomation, blank=True)
	invoked_post_automations = models.ManyToManyField(PostAutomation, blank=True)
	#When these automations are run, they create Actions that contain success/fail data, time
	#of running, etc. Those Actions are FKd to their individual Lead and can be accessed
	#via reverse lookup.
	#Automations are actually run via m2m_changed signal

	def get_fields(self):
		#convenience method for use in the template 
		#for name, value in lead.get_fields: if value, do stuff
		hidelist = ['id', 'distributor', 'invoked_email_automations', 'invoked_post_automations']
		return [(field.verbose_name, field.value_to_string(self)) for field in Lead._meta.get_fields()
			if field.name not in hidelist and hasattr(field, 'verbose_name')]

	class Meta:
		ordering = ['-created_on']

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)




#two receivers, one monitoring m2m_changed on email automations and one on post automations
#necessary because the sender needs to be the intermediate model class; lead.invoked_x_automations.through
#need to hook into m2m_changed instead of post_save because of how django handles saving m2m relationships
#m2m == sent by the individual field instead of the model itself
@receiver(m2m_changed, sender=Lead.invoked_email_automations.through)
def run_email_automations_and_create_email_actions(sender, **kwargs):
	if kwargs['action'] == "post_add":
		lead = kwargs['instance']
		for pk in kwargs['pk_set']: #set of primary keys added to relation
			automation = EmailAutomation.objects.get(pk=pk)
			action, created = EmailAction.objects.get_or_create(automation=automation, 
																lead=lead,
																defaults={'status':'Pending'})
			action.status = automation.run(lead)
			action.save()

@receiver(m2m_changed, sender=Lead.invoked_post_automations.through)
def run_post_automations_and_create_post_actions(sender, **kwargs):
	if kwargs['action'] == "post_add":
		lead = kwargs['instance']
		for pk in kwargs['pk_set']: #set of primary keys added to relation
			automation = PostAutomation.objects.get(pk=pk)
			action, created = PostAction.objects.get_or_create(automation=automation, 
																lead=lead,
																defaults={'status':'Pending'})
			action.status = automation.run(lead)
			action.save()




