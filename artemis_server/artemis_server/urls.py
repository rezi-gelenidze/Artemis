from django.urls import path, include

urlpatterns = [
	path('', include('artemis_core.urls'), name='core')
]