from django.db import models
from ports.models import Lane  # Import Port and Lane models

# Route model for specific routes, which are made up of multiple lanes
class Route(models.Model):
    name = models.CharField(max_length=255)
    total_distance = models.FloatField()
    estimated_duration = models.FloatField()  # In days or hours
    preferred_fuel_type = models.CharField(max_length=50)
    cargo_capacity = models.FloatField()  # Capacity in tons or TEUs
    route_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('seasonal', 'Seasonal'), ('under_construction', 'Under Construction')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Many-to-Many relationship with Lane through RouteLanes
    lanes = models.ManyToManyField(Lane, related_name='routes', through='RouteLanes') # Many-to-many relationship with Lane


    class Meta:
        db_table = "routes"

    def __str__(self):
        return self.name
    
    

# routes/models.py
class RouteLanes(models.Model):
    route = models.ForeignKey(Route, related_name='route_lanes', on_delete=models.CASCADE)
    lane = models.ForeignKey(Lane, related_name='route_lanes', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Route Lane"
        verbose_name_plural = "Route Lanes"
    
    class Meta:
        db_table = "routes_lanes_rel"
    
    def __str__(self):
        return f'{self.route} - {self.lane}'


