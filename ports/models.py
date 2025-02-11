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
