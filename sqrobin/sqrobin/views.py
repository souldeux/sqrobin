from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from profiles.models import Distributor

def home(request):
	return render(request, "home.html")

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			u = form.save()
			d = Distributor.objects.create(user=u)
			messages.add_message(request, messages.SUCCESS, "User Created!")
			return redirect("register") #//TODO: redirect to lead list view
	else:
		form = UserCreationForm()
	return render(request, "register.html", {'form':form})

