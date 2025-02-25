from rest_framework import serializers
from .models import Booking,Tracking,Document
from cargo.serializers import CargoSerializer,ContainerSerializer
from users.serializers import UserSerializer  # Import from users app
from ports.serializers import LaneSerializer  # Import from ports app
from ports.serializers import PortSerializer  # Import PortSerializer
from shipping.serializers import ShippingRoutesSerializer,VoyageSerializer
from ports.models import Port
from cargo.models import Cargo,Container  # Adjust the import path to your Cargo model
from django.utils.timezone import now



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
        fields = [
            'id', 'user', 'cargo', 'lane', 'shipping_route', 'tracking', 'status', 'total_price',
            'arrange_container_haulage', 'pickup_date', 'haulage_reference',
            'stakeholders', 'customer_reference', 'optional_fields'
        ]
    
    def update(self, instance, validated_data):
        # Prevent user_id from being updated
        validated_data.pop('user', None)  # Remove user field if it's in the request
        return super().update(instance, validated_data)

class TrackingSerializer(serializers.ModelSerializer):
    estimated_arrival = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Tracking
        fields = ['id', 'status', 'location', 'estimated_arrival', 'remarks']

    def get_status(self, obj):
        return obj.get_status_display()  # Returns the human-readable status

    def get_estimated_arrival(self, obj):
        """Return estimated arrival in 'X days' format, ensuring past dates return '0 days'."""
        if not obj.estimated_arrival:
            return None  # If no estimated arrival, return None
        
        today = now().date()
        estimated_date = obj.estimated_arrival.date()
        days_remaining = (estimated_date - today).days
        
        return f"{max(days_remaining, 0)} days"  # Ensures no negative values

# Detailed serializer for list_booking API
class BookingDetailSerializer(serializers.ModelSerializer):
    
    container_quantity = serializers.SerializerMethodField()
    container_type = serializers.SerializerMethodField()
    container_weight = serializers.SerializerMethodField()
    commodity = serializers.SerializerMethodField()


    origin = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    price_owner = serializers.SerializerMethodField()
    voyage = VoyageSerializer(source="shipping_route")


    
    
    class Meta:
        model = Booking
        fields = ['id', 'container_quantity', 'origin', 'destination' , 'commodity','container_type', 'container_weight','price_owner','voyage']

    def get_origin(self, obj):
        """Returns origin port with port_name, pincode, and departure_time."""
        port = obj.lane.from_port if obj.lane else None  # Handle missing lane
        shipping_route = obj.shipping_route if obj.shipping_route else None  # Handle missing shipping_route

        if not port:
            return None

        return {
            "port_name": port.port_name,
            "pincode": getattr(port, "pincode", None),  # Handle missing pincode
            "departure_time": shipping_route.departure_time.strftime("%d-%b-%Y %H:%M:%S") if shipping_route and shipping_route.departure_time else None
        }

    def get_destination(self, obj):
        """Returns destination port with port_name, pincode, and formatted arrival_time."""
        port = obj.lane.to_port if obj.lane else None  # Handle missing lane
        shipping_route = obj.shipping_route if obj.shipping_route else None  # Handle missing shipping_route

        if not port:
            return None

        return {
            "port_name": port.port_name,
            "pincode": getattr(port, "pincode", None),  # Handle missing pincode
            "arrival_time": shipping_route.arrival_time.strftime("%d-%b-%Y %H:%M:%S") if shipping_route and shipping_route.arrival_time else None
        }

    def get_container_quantity(self, obj):
        """Calculate total container quantity from cargo containers"""
        if obj.cargo:
            return sum(container.number_of_containers for container in obj.cargo.containers.all())
        return 0

    def get_container_type(self, obj):
        """Extract container types from cargo containers"""
        if obj.cargo:
            return [container.container_type_size for container in obj.cargo.containers.all()]
        return []

    def get_container_weight(self, obj):
        """Calculate total container weight"""
        if obj.cargo:
            return sum(container.weight_per_container * container.number_of_containers for container in obj.cargo.containers.all())
        return 0

    def get_commodity(self, obj):
        """Assuming commodity information can be extracted from cargo description"""
        return obj.cargo.description if obj.cargo else "Unknown"
    
    def get_price_owner(self, obj):
        return "Ximble"  # Hardcoded value
    

class BookingListSerializer(serializers.ModelSerializer):
    customer = UserSerializer(source="user",fields=['id', 'first_name', 'last_name', 'email', 'phone_number', 'organization', 'organization_name'])  

    status = serializers.SerializerMethodField()

    package_details = serializers.SerializerMethodField()  # Nested cargo details
    origin = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()


    tracking = TrackingSerializer()

    order_created_at = serializers.SerializerMethodField()
    status_updated_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'order_created_at', 'status', 'status_updated_at', 'total_price', 'customer', 'package_details', 'origin', 'destination', 'tracking']

    def get_status(self, obj):
        return obj.get_status_display()  # Returns the human-readable status

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
    
    def get_origin(self, obj):
        """Returns origin port with port_name, pincode, and departure_time."""
        port = obj.lane.from_port if obj.lane else None  # Handle missing lane
        shipping_route = obj.shipping_route if obj.shipping_route else None  # Handle missing shipping_route

        if not port:
            return None

        return {
            "port_name": port.port_name,
            "pincode": getattr(port, "pincode", None),  # Handle missing pincode
            "departure_time": shipping_route.departure_time.strftime("%d-%b-%Y %H:%M:%S") if shipping_route and shipping_route.departure_time else None
        }

    def get_destination(self, obj):
        """Returns destination port with port_name, pincode, and formatted arrival_time."""
        port = obj.lane.to_port if obj.lane else None  # Handle missing lane
        shipping_route = obj.shipping_route if obj.shipping_route else None  # Handle missing shipping_route

        if not port:
            return None

        return {
            "port_name": port.port_name,
            "pincode": getattr(port, "pincode", None),  # Handle missing pincode
            "arrival_time": shipping_route.arrival_time.strftime("%d-%b-%Y %H:%M:%S") if shipping_route and shipping_route.arrival_time else None
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
    
