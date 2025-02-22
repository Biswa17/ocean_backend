from rest_framework import serializers
from .models import Booking,Tracking,Document
from cargo.serializers import CargoSerializer,ContainerSerializer
from users.serializers import UserSerializer  # Import from users app
from ports.serializers import LaneSerializer  # Import from ports app
from ports.serializers import PortSerializer  # Import PortSerializer
from ports.models import Port
from cargo.models import Cargo,Container  # Adjust the import path to your Cargo model



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
    documents = DocumentSerializer(many=True)

    
    
    class Meta:
        model = Booking
        fields = ['id', 'status', 'total_price', 'user', 'cargo', 'from_port', 'to_port' , 'documents', 'tracking', 'shipping_route']

class BookingListSerializer(serializers.ModelSerializer):
    customer = UserSerializer(source="user",fields=['id', 'first_name', 'last_name', 'email', 'phone_number', 'organization', 'organization_name'])  

    package_details = serializers.SerializerMethodField()  # Nested cargo details
    origin = PortSerializer(source="lane.from_port", read_only=True)  # Full Port object
    destination = PortSerializer(source="lane.to_port", read_only=True)  # Full Port object

    tracking = TrackingSerializer()

    order_created_at = serializers.SerializerMethodField()
    status_updated_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'order_created_at', 'status', 'status_updated_at', 'total_price', 'customer', 'package_details', 'origin', 'destination', 'tracking', 'shipping_route']

    def get_order_created_at(self, obj):
        return obj.created_at.strftime("%d-%b-%Y %H:%M:%S") if obj.created_at else None

    def get_status_updated_at(self, obj):
        return obj.updated_at.strftime("%d-%b-%Y %H:%M:%S") if obj.updated_at else None

    def get_package_details(self, obj):
        """Custom package details instead of full Cargo object."""
        cargo = obj.cargo  # Get cargo object
        if not cargo:
            return None
        
        # Calculate required values
        total_boxes = sum(container.number_of_containers for container in cargo.containers.all())
        total_weight = sum(container.number_of_containers * container.weight_per_container for container in cargo.containers.all())
        
        # You may need to calculate `volume_weight` and `CFT` based on your business logic
        volume_weight = total_weight * 1.2  # Placeholder formula
        cft = total_boxes * 10  # Placeholder formula

        return {
            "cargo_type": cargo.cargo_type,
            "total_boxes": total_boxes,
            "total_weight": round(total_weight, 2),
            "volume_weight": round(volume_weight, 2),
            "cft": round(cft, 2)
        }



class PortValidationSerializer(serializers.Serializer):
    from_port_id = serializers.IntegerField()
    from_port_inland_transport = serializers.CharField()
    to_port_id = serializers.IntegerField()
    tp_port_inland_transport = serializers.CharField()

    def validate(self, data):
        from_port_id = data.get("from_port_id")
        to_port_id = data.get("to_port_id")
        from_port_inland_transport = data.get("from_port_inland_transport")
        tp_port_inland_transport = data.get("tp_port_inland_transport")

        # Check if from_port_id and to_port_id are provided and valid
        if not from_port_id:
            raise serializers.ValidationError("from_port_id is required.")
        if not to_port_id:
            raise serializers.ValidationError("to_port_id is required.")

        try:
            # Check if the from and to ports exist in the database
            from_port = Port.objects.get(id=from_port_id)
        except Port.DoesNotExist:
            raise serializers.ValidationError(f"Port with ID {from_port_id} does not exist.")

        try:
            to_port = Port.objects.get(id=to_port_id)
        except Port.DoesNotExist:
            raise serializers.ValidationError(f"Port with ID {to_port_id} does not exist.")

        # Check that inland transport details are provided
        if not from_port_inland_transport:
            raise serializers.ValidationError("from_port_inland_transport is required.")
        if not tp_port_inland_transport:
            raise serializers.ValidationError("tp_port_inland_transport is required.")

        return data
    
