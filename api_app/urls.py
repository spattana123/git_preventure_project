from django.urls import path
from .views import BikeHire
from .views import BikeHirePlot

urlpatterns = [
	path('bike-hire/', BikeHire.as_view()),
	path('bike-hire-plot/', BikeHirePlot.as_view()),
]