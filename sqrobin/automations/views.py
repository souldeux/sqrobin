from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from automations.models import EmailAutomation, PostAutomation, EmailAction, PostAction
from automations.forms import EmailAutomationForm, PostAutomationForm

#//TODO: List view for both automation types (include basic statistics on associated actions)
#Should be able to expand any given automation to view its details
#Should be able to click in expanded automation to edit it
#Add new automation button; add/edit function is same as on lead page

#//TODO: Permissions
def email_automation_list_view(request):
	email_automations = EmailAutomation.objects.filter(distributor=request.user.distributor)
	#https://docs.djangoproject.com/en/1.9/topics/pagination/
	#Use built-in pagination module to paginate results, 25 per page
	paginator = Paginator(email_automations, 25)
	page = request.GET.get('page')
	try:
		automations = paginator.page(page)
	except PageNotAnInteger:
		automations = paginator.page(1)
	except EmptyPage:
		automations = paginator.page(paginator.num_pages)

	return render(request, "automations/emailautomationlist.html", {'automations':automations})

def post_automation_list_view(request):
	post_automations = PostAutomation.objects.filter(distributor=request.user.distributor)
	#https://docs.djangoproject.com/en/1.9/topics/pagination/
	#Use built-in pagination module to paginate results, 25 per page
	paginator = Paginator(post_automations, 25)
	page = request.GET.get('page')
	try:
		automations = paginator.page(page)
	except PageNotAnInteger:
		automations = paginator.page(1)
	except EmptyPage:
		automations = paginator.page(paginator.num_pages)
	
	return render(request, "automations/postautomationlist.html", {'automations':automations})

def email_automation_create_edit_view(request):
	#Displays a ModelForm for an EmailAutomation object; if an "instance" is passed via the url, that 
	#instance is loaded into the ModelForm for editing
	instance_id = request.GET.get('instance', None)
	if instance_id is not None:
		instance = EmailAutomation.objects.get(id=instance_id)
		if instance.distributor != request.user.distributor:
			messages.add_message(request, messages.WARNING, "You are not authorized to edit that automation.")
			return redirect("automations:emailautomationlist")
	else:
		instance = None

	if request.method == 'POST':
		form = EmailAutomationForm(request.POST, instance=instance)
		if form.is_valid():
			newautomation = form.save(commit=False)
			newautomation.distributor = request.user.distributor
			newautomation.save()
			messages.add_message(request, messages.SUCCESS, "Automation saved!")
			return redirect(request.POST['request_url'])

	else:
		form = EmailAutomationForm(instance=instance)
	
	return render(request, "automations/emailautomationform.html", {'form':form, 'instance':instance})

def post_automation_create_edit_view(request):
	#Displays a ModelForm for an EmailAutomation object; if an "instance" is passed via the url, that 
	#instance is loaded into the ModelForm for editing
	instance_id = request.GET.get('instance', None)
	if instance_id is not None:
		instance = PostAutomation.objects.get(id=instance_id)
		if instance.distributor != request.user.distributor:
			messages.add_message(request, messages.WARNING, "You are not authorized to edit that automation.")
			return redirect("automations:postautomationlist")
	else:
		instance = None

	if request.method == 'POST':
		form = PostAutomationForm(request.POST, instance=instance)
		if form.is_valid():
			newautomation = form.save(commit=False)
			newautomation.distributor = request.user.distributor
			newautomation.save()
			messages.add_message(request, messages.SUCCESS, "Automation saved!")
			return redirect(request.POST['request_url'])

	else:
		form = PostAutomationForm(instance=instance)
	
	return render(request, "automations/postautomationform.html", {'form':form, 'instance':instance})