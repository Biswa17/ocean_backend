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

    
    
    class Meta:
        model = Booking
        fields = ['id', 'status', 'total_price', 'user', 'cargo', 'from_port', 'to_port' , 'tracking', 'shipping_route']


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


class CargoValidationSerializer(serializers.Serializer):
    cargo_type = serializers.ChoiceField(choices=Cargo.CARGO_TYPE_CHOICES)
    temperature_controlled = serializers.BooleanField()
    dangerous_goods = serializers.BooleanField()

    def validate(self, data):
        cargo_type = data.get("cargo_type")
        temperature_controlled = data.get("temperature_controlled")
        dangerous_goods = data.get("dangerous_goods")

        # Ensure that temperature_controlled and dangerous_goods are booleans
        if not isinstance(temperature_controlled, bool):
            raise serializers.ValidationError("temperature_controlled must be a boolean.")

        if not isinstance(dangerous_goods, bool):
            raise serializers.ValidationError("dangerous_goods must be a boolean.")

        return data

class ContainerValidationSerializer(serializers.Serializer):
    container_type_size = serializers.ChoiceField(choices=Container.CONTAINER_TYPE_SIZE_CHOICES)  # Based on model choices
    container_usage_options = serializers.ListField(
        child=serializers.ChoiceField(choices=Container.USAGE_OPTIONS),  # Validate each option as a valid choice
        required=False,  # Since it's a JSONField and can be empty, we mark it as not required
        allow_empty=True  # Allow an empty list
    )
    number_of_containers = serializers.IntegerField(min_value=1)  # Ensures positive integer
    weight_in_tons = serializers.FloatField(min_value=0.1)  # Ensures positive float (tons)

    def validate(self, data):
        container_usage_options = data.get("container_usage_options")
        weight_in_tons = data.get("weight_in_tons")

        # Ensure weight_in_tons is positive
        if weight_in_tons <= 0:
            raise serializers.ValidationError("weight_in_tons must be a positive value.")

        # Validate container_usage_options (if provided)
        if container_usage_options:
            invalid_options = [option for option in container_usage_options if option not in dict(Container.USAGE_OPTIONS)]
            if invalid_options:
                raise serializers.ValidationError(f"Invalid container_usage_options: {', '.join(invalid_options)}.")

        return data


class BookingCreateValidationSerializer(serializers.Serializer):
    port = PortValidationSerializer()
    cargo = CargoValidationSerializer()
    containers = ContainerValidationSerializer(many=True)

    
