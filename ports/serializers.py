from rest_framework import serializers
from .models import Port

class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ['id', 'port_name', 'location', 'country', 'city', 'state', 'code', 'geo_code', 'type']
