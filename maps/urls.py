from django. urls import path
from .views import calc_distance_view

app_name="maps"

urlpatterns = [
	path('distance',calc_distance_view,name='distance')

]