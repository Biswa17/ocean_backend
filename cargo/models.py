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

    TEMPERATURE_RANGE_CHOICES = [
        ('cold', 'Cold (-20°C to 0°C)'),
        ('cool', 'Cool (0°C to 8°C)'),
        ('ambient', 'Ambient (15°C to 25°C)'),
        ('hot', 'Hot (Above 25°C)')
    ]

    DG_CLASS_CHOICES = [
        ('class_1', 'Explosives'),
        ('class_2', 'Gases'),
        ('class_3', 'Flammable Liquids'),
        ('class_4', 'Flammable Solids'),
        ('class_5', 'Oxidizing Substances'),
        ('class_6', 'Toxic & Infectious Substances'),
        ('class_7', 'Radioactive Materials'),
        ('class_8', 'Corrosives'),
        ('class_9', 'Miscellaneous Dangerous Goods')
    ]

    HAZARDOUS_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk')
    ]

    cargo_type = models.CharField(max_length=50, choices=CARGO_TYPE_CHOICES)
    temperature_controlled = models.BooleanField(default=False)
    dangerous_goods = models.BooleanField(default=False)

    temperature_range = models.CharField(max_length=20, choices=TEMPERATURE_RANGE_CHOICES, null=True, blank=True)
    dg_class = models.CharField(max_length=20, choices=DG_CLASS_CHOICES, null=True, blank=True)
    hazardous_level = models.CharField(max_length=20, choices=HAZARDOUS_LEVEL_CHOICES, null=True, blank=True)

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