from rest_framework import serializers
from .models import Ship,ShippingLiner,ShippingRoutes

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'name', 'registration_number', 'ship_type', 'preferred_fuel_type', 'capacity', 'flag', 'shipping_liner']

class ShippingLinerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingLiner
        fields = ['id', 'name', 'contact_details', 'fleet_size', 'operational_area', 'type_of_vessels', 'rating']


class ShippingRoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRoutes
        fields = ['id', 'route', 'ship', 'pricing_model', 'departure_schedule', 'arrival_schedule', 'liner_vessel_types']
