from rest_framework import serializers
from .models import Booking,Tracking,Document
from cargo.serializers import CargoSerializer
from users.serializers import UserSerializer  # Import from users app
from ports.serializers import LaneSerializer  # Import from ports app
from ports.serializers import PortSerializer  # Import PortSerializer


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'booking', 'document_type', 'document_url', 'note',
            'created_at', 'updated_at'
        ]



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'cargo','lane','shipping_route','tracking', 'status', 'total_price']
    
    def update(self, instance, validated_data):
        # Prevent user_id from being updated
        validated_data.pop('user', None)  # Remove user field if it's in the request
        return super().update(instance, validated_data)

class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ['id', 'status', 'location', 'estimated_arrival', 'remarks']

# Detailed serializer for list_booking API
class BookingDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested user details
    cargo = CargoSerializer()  # Nested cargo details

    from_port = PortSerializer(source="lane.from_port", read_only=True)  # Full Port object
    to_port = PortSerializer(source="lane.to_port", read_only=True)  # Full Port object

    tracking = TrackingSerializer()

    
    
    class Meta:
        model = Booking
        fields = ['id', 'status', 'total_price', 'user', 'cargo', 'from_port', 'to_port' , 'tracking', 'shipping_route']

