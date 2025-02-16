from rest_framework import serializers
from cargo.models import Cargo,Container


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'cargo_type', 'is_temperature_controlled', 'is_dangerous', 'description', 'earliest_departure_date']
        read_only_fields = ['id']

        
class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = [
            'id', 'cargo', 'container_type_size', 'container_options',
            'number_of_containers', 'weight_per_container', 'created_at', 'updated_at'
        ]