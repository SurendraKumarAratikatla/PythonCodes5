from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiCoronaView, name='corona'),
]