
from django.urls import path
from .import views

urlpatterns = [
    path('', views.EventRecord.as_view())
]
