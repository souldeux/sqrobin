from leads.models import Lead
from automations.models import EmailAutomation, PostAutomation
from profiles.models import Distributor



def generate_leads(number_to_generate):
	"""
	Generates a given number of leads with static attributes
	"""
	d = Distributor.objects.get(id=1)
	for i in xrange(0, number_to_generate):
		l = Lead.objects.create(
			distributor = d,
			first_name = "John",
			last_name = str(i+1),
			home_phone = "555-555-5555",
			cell_phone = "555-555-5555",
			business_phone = "555-555-5555",
			email = "test@test.com",
			personal_address = "Test Address Line 1",
			personal_address_2 = "Test Address Line 2",
			personal_city = "Atlanta",
			personal_state = "GA",
			personal_zip = "30064",
			business_address = "Test Business Address Line 1",
			business_address_2 = "Test Business Address Line 2",
			business_city = "Marietta",
			business_state = "GA",
			business_zip = "30064",
			fax_number = "000-999-9999",
			industry = "Fat Stacks",
			position = "Pirate's Plunder",
			website = "http://google.com",
			)
		print l
	return "Complete!"


def generate_email_automations(number_to_generate):
	d = Distributor.objects.get(id=1)
	for i in xrange(0, number_to_generate):
		e = EmailAutomation.objects.create(
			distributor = d,
			recipients = '{"test": "test@test.com", "nick": "nick@test.com"}',
			sender_email = "sq@robin.com",
			subject = "Test Subject",
			body = "Test Body",
			label = "Test Label",
			)
		print e
	return "Complete!"

def generate_post_automations(number_to_generate):
	d = Distributor.objects.get(id=1)
	for i in xrange(0, number_to_generate):
		p = PostAutomation.objects.create(
			distributor = d,
			endpoint = 'http://google.com',
			lead_data = '{"last_name": "val2", "first_name": "val1"}',
			custom_data = '{"key2": "val2", "key1": "val1"}',
			label = 'Test Label',
			)
		print p
	return 'Complete!'