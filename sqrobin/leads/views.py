from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from leads.models import Lead
from profiles.models import Distributor
from leads.forms import LeadForm
from automations.models import EmailAutomation, PostAutomation


#TODO: Permission Decorators

@login_required(login_url='/login/')
def lead_list_view(request):
	#Returns a list of all Lead objects belonging to a requesting user
	lead_list = Lead.objects.filter(distributor=request.user.distributor)

	#https://docs.djangoproject.com/en/1.9/topics/pagination/
	#Use built-in pagination module to paginate results, 25 per page
	paginator = Paginator(lead_list, 25)
	page = request.GET.get('page')
	try:
		leads = paginator.page(page)
	except PageNotAnInteger:
		#If the page isn't an integer, deliver the first page
		leads = paginator.page(1)
	except EmptyPage:
		#If a page is out of range (like 999999), deliver last page of results
		leads = paginator.page(paginator.num_pages)

	return render(request, "leads/leadlist.html", {'leads':leads})

@login_required(login_url='/login/')
def lead_create_edit_view(request):
	#Displays a ModelForm for a Lead object; if an "instance" is passed via the url, that 
	#instance is loaded into the ModelForm for editing
	instance_id = request.GET.get('instance', None)
	if instance_id is not None:
		instance = Lead.objects.get(id=instance_id)
		if instance.distributor != request.user.distributor:
			messages.add_message(request, messages.WARNING, "You are not authorized to edit that lead.")
			return redirect("leads:leadlist") #named URL; make sure patterns match
	else:
		instance = None

	if request.method == 'POST':
		form = LeadForm(request.POST, instance=instance)
		if form.is_valid():
			newlead = form.save(commit=False)
			newlead.distributor = request.user.distributor
			newlead.save()
			form.save_m2m()
			messages.add_message(request, messages.SUCCESS, "Lead saved!")
			return redirect(request.POST['request_url'])

	else:
		form = LeadForm(instance=instance)
	
	#pull these to main indent level so that queryset is restricted both on GET and when re-rendering
	#a form with errors after a bad POST
	form.fields['invoked_email_automations'].queryset = EmailAutomation.objects.filter(distributor=request.user.distributor)
	form.fields['invoked_post_automations'].queryset = PostAutomation.objects.filter(distributor=request.user.distributor)
	
	#http://stackoverflow.com/questions/11276100/how-do-i-insert-a-django-form-in-twitter-bootstrap-modal-window
	return render(request, "leads/leadform.html", {'form':form, 'instance':instance})


def state_to_abbreviation(state_name):
	#Gravity Forms posts full state names; convert to 2-letter abbreviation
	if not state_name:
		return ''

	state_dict = {
		"Alabama": "AL",
		"Alaska": "AK",
		"Arizona": "AZ",
		"Arkansas": "AR",
		"California": "CA",
		"Colorado": "CO",
		"Connecticut": "CT",
		"Deleware": "DE",
		"Florida": "FL",
		"Georgia": "GA",
		"Hawaii": "HI",
		"Idaho": "ID",
		"Illinois": "IL",
		"Indiana": "IN",
		"Iowa": "IA",
		"Kansas": "KS",
		"Kentucky": "KY",
		"Louisiana": "LA",
		"Maine": "ME",
		"Maryland": "MD",
		"Massachusetts": "MA",
		"Michigan": "MI",
		"Minnesota": "MN",
		"Mississippi": "MS",
		"Missouri": "MO",
		"Montana": "MT",
		"Nebraska": "NE",
		"Nevada": "NV",
		"New Hampshire": "NH",
		"New Jersey": "NJ",
		"New Mexico": "NM",
		"New York": "NY",
		"North Carolina": "NC",
		"North Dakota": "ND",
		"Ohio": "OH",
		"Oklahoma": "OK",
		"Oregon": "OR",
		"Pennsylvania": "PA",
		"Rhode Island": "RI",
		"South Carolina": "SC",
		"South Dakota": "SD",
		"Tennessee": "TN",
		"Texas": "TX",
		"Utah": "UT",
		"Vermont": "VT",
		"Virginia": "VA",
		"Washington": "WA",
		"West Virginia": "WV",
		"Wisconsin": "WI",
		"Wyoming": "WY"
	}

	try:
		return state_dict[state_name]
	except KeyError:
		#state name not in dict; DC or some armed forces stuff. screw it they live in texas now.
		#//TODO: don't be this retarded
		return "TX"



@csrf_exempt
def lead_creation_api_endpoint_1_0(request):
	"""
	Versioned (1.0) API endpoint for lead creation. Expects a POST request with lead & distributor data
	"""
	#TODO: make this not a debug thing; requests to this endpoint should NOT becoming from the host server
	#that would mean someone set up a post automation to the lead endpoint, potentially making an infinite loop
	print "Host IP: {}".format(request.get_host())
	ip = request.META.get('HTTP_CF_CONNECTING_IP') 
	if ip is None: 
		ip = request.META.get('REMOTE_ADDR')
	print "Requesting IP: {}".format(ip)
	if str(ip).lower() in str(request.get_host()).lower() or str(request.get_host()).lower() in str(ip).lower():
		return HttpResponse(status=403)#forbidden


	if request.method != "POST":
		return HttpResponse("Method Not Allowed", status=405) #method not allowed
	else:
		#fix our state data
		abbreviated_personal_state = state_to_abbreviation(request.POST.get('personal_state',''))
		abbreviated_business_state = state_to_abbreviation(request.POST.get('business_state', ''))
		#Instantiate a blank lead object and populate it with data from the various stuff we get via POST
		newlead = Lead(
			first_name = request.POST.get('first_name', ''),
			last_name = request.POST.get('last_name', ''),
			home_phone = request.POST.get('home_phone', ''),
			cell_phone = request.POST.get('cell_phone', ''),
			business_phone = request.POST.get('business_phone', ''),
			email = request.POST.get('email', ''),
			personal_address = request.POST.get('personal_address', ''),
			personal_address_2 = request.POST.get('personal_address_2', ''),
			personal_city = request.POST.get('personal_city', ''),
			personal_state = abbreviated_personal_state,
			personal_zip = request.POST.get('personal_zip', ''),
			business_address = request.POST.get('business_address', ''),
			business_address_2 = request.POST.get('business_address_2', ''),
			business_city = request.POST.get('business_city', ''),
			business_state = abbreviated_business_state,
			business_zip = request.POST.get('business_zip', ''),
			fax_number = request.POST.get('fax_number', ''), 	
			industry = request.POST.get('industry', ''),
			position = request.POST.get('position', ''),
			website = request.POST.get('website', ''), 
			dob = request.POST.get('dob', None),
			comments = request.POST.get('comments', ''),
			referral = request.POST.get('referral', ''),
			notes = request.POST.get('notes', ''),
			)				
		
		#Try to associate a distributor with the new lead using the POSTed API key
		#wrap in str() just in case / for testing with UUIDs
		try:
			key = request.POST.get('api_key','')
			newlead.distributor = Distributor.objects.get(api_key=str(key))
		except:
			return HttpResponse("Invalid Distributor Key", status=400) #bad request

		#Call full_clean() BEFORE associating automations to avoid firing them with invalid data
		try:
			newlead.full_clean() #returns None when everything is all good, raises ValidationError otherwise
		except ValidationError, e:
			return HttpResponse("Invalid Data Supplied: {}".format(e), status=400)

		#must save the lead here in order to create database stuff necessary for m2m relationships
		newlead.save()

		for key in request.POST.getlist('invoked_email_automations'):
			try:
				newlead.invoked_email_automations.add(EmailAutomation.objects.get(invocation_key=str(key)))
			except Exception, e:
				return HttpResponse("Error Adding Email Automation: {}".format(Exception, e), status=400)

		for key in request.POST.getlist('invoked_post_automations'):
			try:
				newlead.invoked_post_automations.add(PostAutomation.objects.get(invocation_key=str(key)))
			except Exception, e:
				return HttpResponse("Error Adding POST Automation: {}".format(e), status=400)

		#If we've made it this far, we have a fully populated lead object ready to save.
		newlead.save() #returns None when saved like this, not particularly interesting
		return HttpResponse("Lead Created: {} {}".format(newlead.first_name, newlead.last_name), status=201)



