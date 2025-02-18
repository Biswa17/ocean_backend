from rest_framework import serializers
from cargo.models import Cargo, Container

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'cargo', 'container_type_size', 'number_of_containers', 'weight_per_container', 'container_usage_options']
        read_only_fields = ['id']

class ContainerPartialValidationSerializer(serializers.Serializer):
    container_type_size = serializers.ChoiceField(choices=[choice[0] for choice in Container.CONTAINER_TYPE_SIZE_CHOICES])
    number_of_containers = serializers.IntegerField(min_value=1)
    weight_per_container = serializers.FloatField(min_value=0.1)
    container_usage_options = serializers.ListField(child=serializers.ChoiceField(choices=Container.USAGE_OPTIONS), required=False)


class CargoSerializer(serializers.ModelSerializer):
    containers = ContainerSerializer(many=True, read_only=True)  # Now, ContainerSerializer is defined before use

    class Meta:
        model = Cargo
        fields = ['id', 'cargo_type', 'is_temperature_controlled', 'is_dangerous', 'description', 'earliest_departure_date', 'containers']
        read_only_fields = ['id']
