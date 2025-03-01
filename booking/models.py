from django.db import models


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

    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, related_name='documents',null=True)
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
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('booked', 'Booked'), ('in_transit', 'In Transit'), ('completed', 'Completed'), ('cancelled', 'Cancelled')
    ]
    

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')  # Assuming users app exists
    cargo = models.ForeignKey('cargo.Cargo', on_delete=models.CASCADE, related_name='bookings',null=True, blank=True)
    shipping_route = models.ForeignKey('shipping.ShippingRoutes', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    lane = models.ForeignKey('ports.Lane', related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)
    tracking = models.OneToOneField('Tracking', on_delete=models.SET_NULL, related_name='booking', null=True, blank=True)


    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    # New fields
    arrange_container_haulage = models.ForeignKey('ArrangeContainerYardHaulage', on_delete=models.SET_NULL, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    haulage_reference = models.CharField(max_length=255, null=True, blank=True)  # Optional field

    stakeholders = models.JSONField(null=True, blank=True)
    customer_reference = models.CharField(max_length=255, null=True, blank=True)  # Optional field

    # Many-to-Many relationship for OptionalFields
    optional_fields = models.ManyToManyField("OptionalFields", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"Booking {self.id} - {self.status}"
    
class Tracking(models.Model):
    STATUS_CHOICES = [
        ('order_received', 'Order Received'),
        ('order_preparing', 'Order Being Prepared'),
        ('order_dispatched', 'Order Dispatched'),
        ('in_transit', 'Order in Transit'),
        ('arrived', 'Order Arrived'),
        ('delivered', 'Order Delivered'),
        ('cancelled', 'Order Cancelled')
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


class ArrangeContainerYardHaulage(models.Model):
    name = models.CharField(max_length=255)  # e.g., "K.R.C Container depot"
    address = models.TextField()  # e.g., "96 Moo5, Tungsukhla, Sriracha, Chonburi 96 96"
    city = models.CharField(max_length=255)  # e.g., "Leam Chabang"
    country = models.CharField(max_length=255)  # e.g., "Thailand"
    postal_code = models.CharField(max_length=20)  # e.g., "20230"

    class Meta:
        db_table = "arrange_container_yard_haulage"

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"


class OptionalFields(models.Model):
    service = models.CharField(max_length=255)  # Mandatory field for service name
    cost_per_container = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional cost
    description = models.TextField(null=True, blank=True)  # Optional description

    class Meta:
        db_table = "optional_fields"

    def __str__(self):
        return f"{self.service} - Cost: {self.cost_per_container or 'N/A'}"

