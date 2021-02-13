from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins
from .serializers import  *
from django.http import HttpResponse, JsonResponse
from .models import *
from .soup import *

class DailyUpdates(View):
    def get(self,request,*args,**kwargs):
        now = datetime.now()
        time = now.strftime("%H")
        print(time)
        if time=="5":
            cities = Cities.objects.all()
            for c in cities:
                print(c.id, c.c_name)
                city_events(c.c_name)
            print("Daily Update Done!")
            return HttpResponse("Daily Update Done!")
        else:
            return HttpResponse("Not Correct Time")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print("returning FORWARDED_FOR")
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        print("returning REAL_IP")
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        print("returning REMOTE_ADDR")
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Cityevents(generics.GenericAPIView):
    def get(self,request, *args, **kwargs):
        ip = get_client_ip(request)
        try:
            city_events(kwargs["cname"])
        except:
            return JsonResponse({"msg":"Some error happened. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            evs = Cities.objects.get(c_name=kwargs["cname"])
        except:
            md = f"City not found. Check from: http://{request.META['HTTP_HOST']}/events/cities/"
            return JsonResponse({"msg":md}, status=status.HTTP_404_NOT_FOUND)
        try:
            file = open(f'{evs.c_file}','r')
        except:
            return JsonResponse({"msg":"Some error happened. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        seri = json.load(file)
        # print(seri)
        seri["ip"]= ip
        return JsonResponse(seri,status=status.HTTP_200_OK,safe=False)


class City(APIView):
    def get(self,request,format=None,*args,**kwargs):
        # create_cities()
        queryset = Cities.objects.all()
        seri = CitySerializer(queryset,many=True)
        print(seri.data)
        return JsonResponse(seri.data,status=status.HTTP_200_OK,safe=False)

    # def delete(self,request,format=None,*args,**kwargs):
    #     Cities.objects.all().delete()
    #     return Response({"msg":"Kaam Ho gaya"}, status=status.HTTP_200_OK)

def create_cities():
    file = open("cities.json")
    cts = json.load(file)
    for i in cts:
        Cities.objects.create(c_name=i,c_url=f"https://in.bookmyshow.com/explore/home/{i}",c_file=f"Citywise-data/{i}.json")
    print("City creation complete")

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
