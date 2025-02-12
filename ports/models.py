from django.db import models

class Port(models.Model):
    port_name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    geo_code = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        max_length=50,
        choices=[("inland port", "Inland Port"), ("sea port", "Sea Port")],
        default="sea port",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ports"

    def __str__(self):
        return self.port_name


class Yard(models.Model):
    yard_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    geo_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "yards"

    def __str__(self):
        return self.yard_name



class Lane(models.Model):
    # Primary Key
    id = models.AutoField(primary_key=True)
    
    # Foreign Keys referencing Ports for origin and destination
    from_port = models.ForeignKey(Port, related_name='from_ports', on_delete=models.CASCADE)
    to_port = models.ForeignKey(Port, related_name='to_ports', on_delete=models.CASCADE)
    
    # Additional Fields
    distance = models.PositiveIntegerField()  # Distance between ports (in kilometers, miles, etc.)
    estimated_travel_time = models.PositiveIntegerField(help_text="Estimated travel time in days or hours")
    lane_status = models.CharField(
        max_length=50, 
        choices=[
            ('active', 'Active'),
            ('maintenance', 'Maintenance'),
            ('closed', 'Closed')
        ],
        default='active'
    )
    
    # Timestamps for record creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # String representation of the Lane model
    def __str__(self):
        return f"Lane from {self.from_port} to {self.to_port}"
    
    class Meta:
        # Optional: You could add additional constraints or indexes if needed.
        db_table = "lanes"

