from django.shortcuts import render
from .models import Notification
# Create your views here.

def notif(request):
	all_notes = Notification.objects.all().order_by("-time")
	return {"notifications":all_notes}