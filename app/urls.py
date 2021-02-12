
from django.urls import path
from .import views

urlpatterns = [
    path('', views.EventRecord.as_view()),
    path('update',views.DailyUpdates.as_view()),
    path('cities/<str:cname>/',views.Cityevents.as_view()),
    path('cities/',views.City.as_view())
]
