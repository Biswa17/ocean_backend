from django.core.management.base import BaseCommand
from ports.models import Port, Lane
from routes.models import Route
from shipping.models import Ship, ShippingLiner, ShippingRoutes
from users.models import Organization, User
from django.utils import timezone
import random
from django.db import connection

class Command(BaseCommand):
    help = 'Fill all tables with dummy data'

    def handle(self, *args, **kwargs):
        self.truncate_tables()
        self.populate_organizations()
        self.populate_users()
        self.populate_ports()
        self.populate_lanes()
        self.populate_routes()
        self.populate_shipping_liners()
        self.populate_ships()
        self.populate_shipping_routes()
        self.stdout.write(self.style.SUCCESS('All tables populated with dummy data!'))
    
    def truncate_tables(self):
        """Truncate all tables before inserting new data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE ports RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE lanes RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE routes RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE ships RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE shippingliners RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE shipping_routes_rel RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE organizations RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")

        self.stdout.write(self.style.WARNING('All tables truncated successfully!'))

    def populate_ports(self):
        ports_data = [
            {"port_name": "Mumbai Port", "code": "INBOM", "country": "India", "city": "Mumbai", "state": "Maharashtra", "type": "sea port"},
            {"port_name": "Chennai Port", "code": "INMAA", "country": "India", "city": "Chennai", "state": "Tamil Nadu", "type": "sea port"},
            {"port_name": "Kolkata Port", "code": "INKOL", "country": "India", "city": "Kolkata", "state": "West Bengal", "type": "sea port"},
            {"port_name": "Durban Port", "code": "ZADUR", "country": "South Africa", "city": "Durban", "state": "KwaZulu-Natal", "type": "sea port"},
            {"port_name": "Cape Town Port", "code": "ZACTP", "country": "South Africa", "city": "Cape Town", "state": "Western Cape", "type": "sea port"},
            {"port_name": "Lagos Port", "code": "NGLOS", "country": "Nigeria", "city": "Lagos", "state": "Lagos", "type": "sea port"},
            {"port_name": "Mombasa Port", "code": "KENBO", "country": "Kenya", "city": "Mombasa", "state": "Coast", "type": "sea port"},
            {"port_name": "Sydney Port", "code": "AUSYD", "country": "Australia", "city": "Sydney", "state": "New South Wales", "type": "sea port"},
            {"port_name": "Melbourne Port", "code": "AUMEL", "country": "Australia", "city": "Melbourne", "state": "Victoria", "type": "sea port"},
            {"port_name": "Perth Port", "code": "AUPER", "country": "Australia", "city": "Perth", "state": "Western Australia", "type": "sea port"}
        ]
        for port in ports_data:
            Port.objects.get_or_create(**port)
        self.stdout.write(self.style.SUCCESS('Ports data populated successfully!'))

    def populate_lanes(self):
        lanes_data = [
            {"from_port": "INBOM", "to_port": "ZADUR", "distance": 7000, "estimated_travel_time": 14, "lane_status": "active"},
            {"from_port": "INBOM", "to_port": "ZACTP", "distance": 7500, "estimated_travel_time": 15, "lane_status": "active"},
            {"from_port": "INBOM", "to_port": "NGLOS", "distance": 5000, "estimated_travel_time": 10, "lane_status": "active"},
            {"from_port": "INBOM", "to_port": "KENBO", "distance": 6000, "estimated_travel_time": 12, "lane_status": "active"},
            {"from_port": "INMAA", "to_port": "ZADUR", "distance": 6800, "estimated_travel_time": 14, "lane_status": "active"},
            {"from_port": "INMAA", "to_port": "ZACTP", "distance": 7200, "estimated_travel_time": 15, "lane_status": "active"},
            {"from_port": "INKOL", "to_port": "ZADUR", "distance": 7300, "estimated_travel_time": 15, "lane_status": "active"},
            {"from_port": "INKOL", "to_port": "ZACTP", "distance": 7700, "estimated_travel_time": 16, "lane_status": "active"},
            {"from_port": "INBOM", "to_port": "AUSYD", "distance": 8000, "estimated_travel_time": 17, "lane_status": "active"},
            {"from_port": "INMAA", "to_port": "AUMEL", "distance": 8500, "estimated_travel_time": 18, "lane_status": "active"},
            {"from_port": "INKOL", "to_port": "AUSYD", "distance": 8200, "estimated_travel_time": 18, "lane_status": "active"},
            {"from_port": "INKOL", "to_port": "AUPER", "distance": 8500, "estimated_travel_time": 19, "lane_status": "maintenance"},
            {"from_port": "AUSYD", "to_port": "INBOM", "distance": 8000, "estimated_travel_time": 17, "lane_status": "active"},
            {"from_port": "AUMEL", "to_port": "INBOM", "distance": 8500, "estimated_travel_time": 18, "lane_status": "active"}
        ]
        for lane in lanes_data:
            from_port = Port.objects.get(code=lane["from_port"])
            to_port = Port.objects.get(code=lane["to_port"])
            Lane.objects.get_or_create(
                from_port=from_port,
                to_port=to_port,
                distance=lane["distance"],
                estimated_travel_time=lane["estimated_travel_time"],
                lane_status=lane["lane_status"]
            )
        self.stdout.write(self.style.SUCCESS('Lanes data populated successfully!'))

    def populate_routes(self):
        routes_data = [
            {"name": "India to South Africa", "total_distance": 7000, "estimated_duration": 14, "preferred_fuel_type": "Diesel", "cargo_capacity": 10000, "route_status": "active"},
        ]
        for route_data in routes_data:
            Route.objects.get_or_create(**route_data)
        self.stdout.write(self.style.SUCCESS('Routes data populated successfully!'))

    def populate_shipping_liners(self):
        liners_data = [
            {"name": "Maersk Line", "contact_details": "contact@maersk.com", "fleet_size": 700, "operational_area": "Global", "type_of_vessels": "Container Ships", "rating": 9},
            {"name": "MSC", "contact_details": "contact@msc.com", "fleet_size": 600, "operational_area": "Global", "type_of_vessels": "Bulk Carriers", "rating": 8},
        ]
        for liner in liners_data:
            ShippingLiner.objects.get_or_create(**liner)
        self.stdout.write(self.style.SUCCESS('Shipping Liners data populated successfully!'))

    def populate_ships(self):
        liners = list(ShippingLiner.objects.all())
        ships_data = [
            {"name": "Ever Given", "registration_number": "EG12345", "ship_type": "Container Ship", "capacity": 20000, "flag": "Panama", "shipping_liner": random.choice(liners)},
            {"name": "MSC Oscar", "registration_number": "MSC98765", "ship_type": "Container Ship", "capacity": 19000, "flag": "Liberia", "shipping_liner": random.choice(liners)},
        ]
        for ship_data in ships_data:
            Ship.objects.get_or_create(**ship_data)
        self.stdout.write(self.style.SUCCESS('Ships data populated successfully!'))

    def populate_shipping_routes(self):
        routes = list(Route.objects.all())
        ships = list(Ship.objects.all())
        routes_data = [
            {"route": random.choice(routes), "ship": random.choice(ships), "pricing_model": "per_teu", "departure_schedule": ["2025-03-01T10:00:00Z"], "arrival_schedule": ["2025-03-15T18:00:00Z"], "liner_vessel_types": "Container Ships"},
        ]
        for route_data in routes_data:
            ShippingRoutes.objects.get_or_create(**route_data)
        self.stdout.write(self.style.SUCCESS('Shipping Routes data populated successfully!'))

    def populate_organizations(self):
        # Create the organization "Bata"
        bata_organization, created = Organization.objects.get_or_create(organization_name="Bata")
        if created:
            self.stdout.write(self.style.SUCCESS('Organization "Bata" created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Organization "Bata" already exists!'))

    def populate_users(self):
        # Get the "Bata" organization
        try:
            bata_organization = Organization.objects.get(organization_name="Bata")
        except Organization.DoesNotExist:
            self.stdout.write(self.style.ERROR('Organization "Bata" does not exist!'))
            return

        # Create the root user (superuser)
        root_user = User.objects.create_superuser(
            username="tech@ximble",
            email="tech@ximble",
            phone_number="1234567890",
            password="ximble"
        )
        self.stdout.write(self.style.SUCCESS('Root user "tech@ximble" created successfully!'))

        # Create a few more dummy users with the "Bata" organization
        dummy_users_data = [
            {"username": "john_doe", "email": "john@ximble", "phone_number": "1234567891", "password": "password123"},
            {"username": "alice_smith", "email": "alice@ximble", "phone_number": "1234567892", "password": "password123"},
            {"username": "bob_jones", "email": "bob@ximble", "phone_number": "1234567893", "password": "password123"},
        ]
        for user_data in dummy_users_data:
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                phone_number=user_data["phone_number"],
                organization=bata_organization,
                password=user_data["password"]
            )
            self.stdout.write(self.style.SUCCESS(f'User "{user.username}" created successfully!'))
