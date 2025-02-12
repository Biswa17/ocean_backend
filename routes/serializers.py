from rest_framework import serializers
from ports.models import Port, Lane  # Import Port and Lane models
from .models import Route, ShippingLiner, ShippingLinerRoutes


class RouteSerializer(serializers.ModelSerializer):
    lanes = LaneSerializer(many=True)  # Include all lanes for the route

    class Meta:
        model = Route
        fields = '__all__'

class ShippingLinerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingLiner
        fields = '__all__'

class ShippingLinerRoutesSerializer(serializers.ModelSerializer):
    liner = ShippingLinerSerializer()
    route = RouteSerializer()

    class Meta:
        model = ShippingLinerRoutes
        fields = '__all__'
