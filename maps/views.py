from django.shortcuts import render , get_object_or_404
from .models import Measurements
from .forms import MeasurementModelForm
def calc_distance_view(request):
	obj = get_object_or_404(Measurements,id=1)
	form =  MeasurementModelForm(request.POST or None)

	context = {
		"distance":obj,
		"form":form,
	}
	return render(request,"measurements/map.html",context)