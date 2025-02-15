from rest_framework import serializers
from .models import Cargo, Booking,Tracking
from users.serializers import UserSerializer  # Import from users app
from ports.serializers import LaneSerializer  # Import from ports app
from ports.serializers import PortSerializer  # Import PortSerializer
from ports.models import Port  # Import Port model

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'type', 'description', 'weight', 'teu', 'pricing_model', 'price']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'cargo','lane','shipping_route','tracking', 'status', 'total_price']

class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ['id', 'status', 'location', 'estimated_arrival', 'remarks']

# Detailed serializer for list_booking API
class BookingDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user details
    cargo = CargoSerializer()  # Nested cargo details

    from_port = serializers.CharField(source="lane.from_port.port_name", read_only=True)
    to_port = serializers.CharField(source="lane.to_port.port_name", read_only=True)

    tracking = TrackingSerializer()

    
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'cargo', 'from_port', 'to_port' ,'shipping_route', 'status', 'total_price','tracking']

