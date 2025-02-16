from django.db import models


class Cargo(models.Model):
    CARGO_TYPE_CHOICES = [
        ('fabrics', 'Fabrics'),
        ('electronics', 'Electronics'),
        ('machinery', 'Machinery'),
        ('general', 'General Cargo'),
        ('hazardous', 'Hazardous Materials'),
        ('refrigerated', 'Refrigerated Goods'),
    ]

    cargo_type = models.CharField(max_length=50, choices=CARGO_TYPE_CHOICES)
    is_temperature_controlled = models.BooleanField(default=False)
    is_dangerous = models.BooleanField(default=False)

    description = models.TextField(null=True, blank=True)
    earliest_departure_date = models.DateField(null=True, blank=True)  # New Field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cargo"

    def __str__(self):
        return f"Cargo {self.id} - {self.cargo_type}"


class Container(models.Model):
    CONTAINER_TYPE_SIZE_CHOICES = [
        ('20ft_standard', '20ft Standard Container'),
        ('40ft_standard', '40ft Standard Container'),
        ('20ft_reefer', '20ft Refrigerated Container'),
        ('40ft_reefer', '40ft Refrigerated Container'),
        ('flat_rack', 'Flat Rack Container'),
        ('open_top', 'Open Top Container'),
        ('tank', 'Tank Container'),
        ('custom', 'Custom Size'),
    ]

    USAGE_OPTIONS = [
        ('shipper_container', "I want to use a shipper's container."),
        ('import_return', "I want to use an import return or triangular container."),
        ('oversized', "This cargo is oversized."),
    ]

    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='containers')

    container_type_size = models.CharField(max_length=50, choices=CONTAINER_TYPE_SIZE_CHOICES)
    number_of_containers = models.IntegerField()
    weight_per_container = models.FloatField()  # Weight per container in tons
    container_usage_options = models.JSONField(default=list, blank=True)  # Stores multi-select choices

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "container"

    def __str__(self):
        return f"Container {self.id} - {self.container_type_size}"