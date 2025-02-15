from django.db import models


class Cargo(models.Model):
    TYPE_CHOICES = [
        ('general', 'General'),
        ('hazardous', 'Hazardous'),
        ('refrigerated', 'Refrigerated'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # Weight in tons
    teu = models.IntegerField(null=True, blank=True)  # TEU count if applicable
    pricing_model = models.CharField(
        max_length=100, 
        choices=[('per_teu', 'Per TEU'), ('per_ton', 'Per Ton'), ('flat_rate', 'Flat Rate')]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Final price after calculation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cargo"

    def __str__(self):
        return f"Cargo {self.id} - {self.description}"


class Booking(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')  # Assuming users app exists
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='bookings',null=True, blank=True)
    shipping_route = models.ForeignKey('shipping.ShippingRoutes', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    lane = models.ForeignKey('ports.Lane', related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=50, choices=[('draft', 'Draft'),('pending', 'Pending'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='draft')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"Booking {self.id} - {self.status}"
