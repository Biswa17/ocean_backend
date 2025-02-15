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


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('bill_of_lading', 'Bill of Lading'),
        ('freight_invoice', 'Freight Invoice'),
        ('customs_declaration', 'Customs Declaration'),
        ('certificate_of_origin', 'Certificate of Origin'),
        ('insurance_certificate', 'Insurance Certificate'),
        ('packing_list', 'Packing List'),
        ('proof_of_delivery', 'Proof of Delivery (POD)'),
        ('booking_confirmation', 'Booking Confirmation'),
        ('commercial_invoice', 'Commercial Invoice'),
        ('special_handling_instructions', 'Special Handling Instructions'),
    ]

    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_url = models.CharField(max_length=500, null=True, blank=True)  # Stores the file URL instead of a file
    note = models.TextField(null=True, blank=True)  # Any remarks

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "document"

    def __str__(self):
        return f"Document {self.id} - {self.document_type}"



class Booking(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')  # Assuming users app exists
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='bookings',null=True, blank=True)
    shipping_route = models.ForeignKey('shipping.ShippingRoutes', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    lane = models.ForeignKey('ports.Lane', related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)
    tracking = models.OneToOneField('Tracking', on_delete=models.SET_NULL, related_name='booking', null=True, blank=True)


    status = models.CharField(max_length=50, choices=[('draft', 'Draft'),('pending', 'Pending'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='draft')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"Booking {self.id} - {self.status}"
    
class Tracking(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('in_transit', 'In Transit'),
        ('arrived', 'Arrived'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='initiated')
    location = models.CharField(max_length=255, null=True, blank=True)  # Latest location
    estimated_arrival = models.DateTimeField(null=True, blank=True)  # Estimated delivery date/time
    remarks = models.TextField(null=True, blank=True)  # Optional comments

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "tracking"

    def __str__(self):
        return f"Tracking {self.id} - {self.status}"

