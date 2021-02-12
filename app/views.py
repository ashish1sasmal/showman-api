from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins
from .serializers import  *
from django.http import HttpResponse
from .models import *
from .soup import *

class DailyUpdates(View):
    def get(self,request,*args,**kwargs):
        now = datetime.now()
        time = now.strftime("%H")
        print(time)
        if time=="10":
            cities = Cities.objects.all()
            for c in cities:
                print(c.id, c.c_name)
                city_events(c.c_name)
            print("Daily Update Done!")
            return HttpResponse("Daily Update Done!")
        else:
            return HttpResponse("Not Correct Time")

class Cityevents(generics.GenericAPIView):
    def get(self,request, *args, **kwargs):
        print(kwargs)
        try:
            city_events(kwargs["cname"])
        except:
            return Response({"msg":"Some error happened. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            evs = Cities.objects.get(c_name=kwargs["cname"])
        except:
            return Response({"msg":"City not found\nCheck from: http://localhost:8000/events/cities/"}, status=status.HTTP_404_NOT_FOUND)
        try:
            file = open(f'{evs.c_file}','r')
        except:
            return Response({"msg":"Some error happened. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        seri = json.load(file)
        print(seri)
        return Response(seri, status=status.HTTP_200_OK)


class City(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = CitySerializer
    queryset = Cities.objects.all()
    def get(self,request,format=None,*args,**kwargs):
        Cities.objects.all().delete()
        print("Kaam Ho gaya")
        return self.list(request,*args,**kwargs)

    def delete(self,request,format=None,*args,**kwargs):
        Cities.objects.all().delete()
        return Response({"msg":"Kaam Ho gaya"}, status=status.HTTP_200_OK)


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
