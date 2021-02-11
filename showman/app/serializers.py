from .models import *

from rest_framework import serializers


class TimestampSerializer(serializers.ModelSerializer):
    created_on = serializers.ReadOnlyField()
    class Meta:
        model = Timestamp
        fields = ['created_on','updated_on']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ['c_name']

class EventSerializer(serializers.ModelSerializer):
    # created_on = serializers.ReadOnlyField()
    # city = CitySerializer(many=True)
    city = serializers.PrimaryKeyRelatedField(many=True, read_only=False,queryset=Cities.objects.all())

    class Meta:
        model = Events
        fields = ['city','e_id','title','e_url','img_url','created_on','updated_on']
