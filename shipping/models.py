from django.db import models
from routes.models import Route


# Ship model representing individual ships
class Ship(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255, unique=True)
    ship_type = models.CharField(max_length=100)
    preferred_fuel_type = models.CharField(max_length=50,default="Diesel")
    capacity = models.FloatField()  # Capacity in TEUs or tons
    flag = models.CharField(max_length=100)  # Country or flag state
    shipping_liner = models.ForeignKey('ShippingLiner', on_delete=models.CASCADE, related_name='ships')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ships"

    def __str__(self):
        return self.name


# ShippingLiner model for shipping companies
class ShippingLiner(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    fleet_size = models.IntegerField()
    operational_area = models.CharField(max_length=255)
    type_of_vessels = models.CharField(max_length=255)
    rating = models.IntegerField()  # Performance rating out of 10

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shippingliners"

    def __str__(self):
        return self.name


# ShippingLinerRoutes model for linking routes with shipping liners
class ShippingRoutes(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)  # Associate ship with a route
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Voyage price
    voyage_number = models.CharField(max_length=50, unique=True)  # Unique voyage number
    departure_time = models.DateTimeField()  # Single departure datetime
    arrival_time = models.DateTimeField()  # Single arrival datetime
    liner_vessel_types = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shipping_routes_rel"

    def __str__(self):
        return f" {self.route.name} with {self.ship.name}"

