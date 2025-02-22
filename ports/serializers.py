from rest_framework import serializers
from .models import Port,Lane

class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ['id', 'port_name', 'location','pincode' ,'country', 'city', 'state', 'code', 'geo_code', 'type']


class LaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lane
        fields = ['id', 'from_port', 'to_port', 'distance', 'estimated_travel_time', 'lane_status']
