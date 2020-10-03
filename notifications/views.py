from django.shortcuts import render
from .models import Notification
# Create your views here.

def notifications(request):
	notes = Notification.objects.all()
	return render(request,"notifications/allnotifications.html",{"notes":notes})