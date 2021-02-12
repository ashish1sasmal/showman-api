from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins
from .serializers import  EventSerializer
from django.http import HttpResponse
from .models import *
from .soup import *

class DailyUpdates(View):
    def get(self,request,*args,**kwargs):
        now = datetime.now()
        time = now.strftime("%H")
        print(time)
        if time=="08":
            cities = Cities.objects.all()
            for c in cities:
                print(c.id, c.c_name)
                city_events(c.c_name)
            print("Daily Update Done!")
            return HttpResponse("Daily Update Done!")
        else:
            return HttpResponse("Not Correct Time")



class EventRecord(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = EventSerializer
    queryset = Events.objects.all()
    def get(self,request,format=None,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,format=None):
        seri = EventSerializer(data=request.data)
        print(request.data)
        if seri.is_valid():
            seri.save()
            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)
