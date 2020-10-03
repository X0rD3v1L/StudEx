from django.shortcuts import render
from bbanalyser.models import SubjectModel,FolderModel
# from django.utils import simplejson
def options(request):
	# Sorting Time_Dic
	from Time_Dic import time
	time = dict(sorted(time.items(), key=lambda x: x[0]))
	for s in time:
		time[s] = dict(sorted(time[s].items(), key=lambda x: int(x[0].split(".")[0]) if "." in x[0] else 111))
	data = {}
	for s in time:
		data[s] = []
		for f in time[s]:
			data[s].append(f)
	return render(request,'bbanalyser/index.html',{"time":time,"data":data})