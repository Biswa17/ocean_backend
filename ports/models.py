from django.db import models

class Port(models.Model):
    port_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)  # Optional: Additional information about the port's location.
    country = models.CharField(max_length=100, null=True, blank=True)  # Optional: Country where the port is located.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ports'  # Specify the table name explicitly

    def __str__(self):
        return self.port_name
