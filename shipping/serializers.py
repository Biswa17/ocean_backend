from rest_framework import serializers
from .models import Ship,ShippingLiner,ShippingRoutes
import random

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
        fields = ['id', 'route', 'ship', 'pricing_model', 'departure_time', 'arrival_time', 'liner_vessel_types']



class VoyageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    departs = serializers.SerializerMethodField()
    departure_port_name = serializers.SerializerMethodField()
    arrives = serializers.SerializerMethodField()
    arrival_port_name = serializers.SerializerMethodField()
    vessel = serializers.CharField(source='ship.name')
    voyage_number = serializers.CharField()
    container_gate_in_deadline = serializers.SerializerMethodField()
    pricing = serializers.DecimalField(max_digits=10, decimal_places=2, source='price')
    
    
    class Meta:
        model = ShippingRoutes
        fields = [
            'id',
            'departs',
            'departure_port_name',
            'arrives',
            'arrival_port_name',
            'vessel',
            'voyage_number',
            'container_gate_in_deadline',
            'pricing',
            
        ]

    def get_departs(self, obj):
        return obj.departure_time.strftime("%d %b %Y")

    def get_arrives(self, obj):
        return obj.arrival_time.strftime("%d %b %Y")

    def get_container_gate_in_deadline(self, obj):
        return obj.departure_time.strftime("%d %b %Y, %H:%M")

    def get_departure_port_name(self, obj):
        # Get lane from context since it's passed in the API view
        lane = self.context.get("lane")
        return lane.from_port.port_name if lane and lane.from_port else None

    def get_arrival_port_name(self, obj):
        lane = self.context.get("lane")
        return lane.to_port.port_name if lane and lane.to_port else None