from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from leads.models import Lead
from leads.forms import LeadForm
from automations.models import EmailAutomation, PostAutomation


#TODO: Permission Decorators

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