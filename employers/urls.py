from django.urls import path 
from .views import employer_view

app_name = 'employers'


urlpatterns = [
    path('recruit/', employer_view, name='employer')
]
