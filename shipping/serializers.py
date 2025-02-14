from rest_framework import serializers
from .models import Ship,ShippingLiner

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'name', 'registration_number', 'ship_type', 'preferred_fuel_type', 'capacity', 'flag', 'shipping_liner']

class ShippingLinerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingLiner
        fields = ['id', 'name', 'contact_details', 'fleet_size', 'operational_area', 'type_of_vessels', 'rating']
