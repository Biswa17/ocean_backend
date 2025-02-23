from django.core.management.base import BaseCommand
from ports.models import Port, Lane
from routes.models import Route,RouteLanes
from shipping.models import Ship, ShippingLiner, ShippingRoutes
from users.models import Organization, User
from booking.models import Booking,Tracking,Document
from django.utils import timezone
import random
from django.db import connection
from datetime import datetime, timedelta
import random
from cargo.models import Cargo,Container
import uuid


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
        self.create_booking()
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
            cursor.execute("TRUNCATE TABLE document RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE booking RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE tracking RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE cargo RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE container RESTART IDENTITY CASCADE;")


        self.stdout.write(self.style.WARNING('All tables truncated successfully!'))

    def populate_ports(self):
        ports_data = [
            {"port_name": "Mumbai Port", "code": "INBOM", "country": "India", "city": "Mumbai", "state": "Maharashtra", "pincode": "400001", "type": "sea port"},
            {"port_name": "Chennai Port", "code": "INMAA", "country": "India", "city": "Chennai", "state": "Tamil Nadu", "pincode": "600001", "type": "sea port"},
            {"port_name": "Kolkata Port", "code": "INKOL", "country": "India", "city": "Kolkata", "state": "West Bengal", "pincode": "700001", "type": "sea port"},
            {"port_name": "Durban Port", "code": "ZADUR", "country": "South Africa", "city": "Durban", "state": "KwaZulu-Natal", "pincode": "4001", "type": "sea port"},
            {"port_name": "Cape Town Port", "code": "ZACTP", "country": "South Africa", "city": "Cape Town", "state": "Western Cape", "pincode": "8001", "type": "sea port"},
            {"port_name": "Lagos Port", "code": "NGLOS", "country": "Nigeria", "city": "Lagos", "state": "Lagos", "pincode": "100001", "type": "sea port"},
            {"port_name": "Mombasa Port", "code": "KENBO", "country": "Kenya", "city": "Mombasa", "state": "Coast", "pincode": "80100", "type": "sea port"},
            {"port_name": "Sydney Port", "code": "AUSYD", "country": "Australia", "city": "Sydney", "state": "New South Wales", "pincode": "2000", "type": "sea port"},
            {"port_name": "Melbourne Port", "code": "AUMEL", "country": "Australia", "city": "Melbourne", "state": "Victoria", "pincode": "3000", "type": "sea port"},
            {"port_name": "Perth Port", "code": "AUPER", "country": "Australia", "city": "Perth", "state": "Western Australia", "pincode": "6000", "type": "sea port"}
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
            {
                "name": "India to South Africa",
                "total_distance": 7000,
                "estimated_duration": 14,
                "route_status": "active",
                "lanes": [("INBOM", "ZADUR"), ("INBOM", "ZACTP"), ("INBOM", "NGLOS")]  # Lane data
            },
            {
                "name": "India to Australia",
                "total_distance": 8000,
                "estimated_duration": 17,
                "route_status": "active",
                "lanes": [("INBOM", "AUSYD"), ("INMAA", "AUMEL")]  # Lane data
            },
            {
                "name": "India to Kenya",
                "total_distance": 6000,
                "estimated_duration": 12,
                "route_status": "active",
                "lanes": [("INBOM", "KENBO")]  # Lane data
            },
            {
                "name": "India to Middle East",
                "total_distance": 7500,
                "estimated_duration": 15,
                "route_status": "active",
                "lanes": [("INBOM", "ZACTP"), ("INBOM", "NGLOS")]  # Lane data
            },
            {
                "name": "India to Europe",
                "total_distance": 8500,
                "estimated_duration": 18,
                "route_status": "active",
                "lanes": [("INMAA", "ZACTP"), ("INKOL", "ZADUR"), ("INKOL", "ZACTP")]  # Lane data
            },
            {
                "name": "India to Africa",
                "total_distance": 7800,
                "estimated_duration": 16,
                "route_status": "active",
                "lanes": [("INMAA", "ZADUR"), ("INKOL", "ZACTP"), ("INBOM", "ZACTP")]  # Lane data (reuse of ZACTP)
            },
            {
                "name": "India to South America",
                "total_distance": 9000,
                "estimated_duration": 19,
                "route_status": "active",
                "lanes": [("INBOM", "AUSYD"), ("INKOL", "AUPER"), ("INMAA", "ZADUR"), ("INKOL", "ZACTP")]  # Lane data (reuse of INKOL-ZACTP)
            },
            {
                "name": "India to Southeast Asia",
                "total_distance": 7000,
                "estimated_duration": 14,
                "route_status": "active",
                "lanes": [("INBOM", "NGLOS"), ("INMAA", "ZACTP"), ("INKOL", "AUSYD")]  # Lane data
            }
        ]

        
        for route_data in routes_data:
            # Create the route without lanes
            route, created = Route.objects.get_or_create(
                name=route_data["name"], 
                total_distance=route_data["total_distance"],
                estimated_duration=route_data["estimated_duration"],
                route_status=route_data["route_status"]
            )
            
            # Print success message for route creation
            if created:
                self.stdout.write(self.style.SUCCESS(f'Route "{route.name}" created successfully!'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Route "{route.name}" already exists!'))
            
            # Add lanes to the route
            for lane_tuple in route_data["lanes"]:
                from_port = Port.objects.get(code=lane_tuple[0])  # Get the 'from' port
                to_port = Port.objects.get(code=lane_tuple[1])  # Get the 'to' port
                lane, lane_created = Lane.objects.get_or_create(from_port=from_port, to_port=to_port)

                # Create or get the lane association between the route and the lane
                RouteLanes.objects.get_or_create(route=route, lane=lane)
            
            self.stdout.write(self.style.SUCCESS(f'Lanes for Route "{route.name}" added successfully!'))
        
        self.stdout.write(self.style.SUCCESS('Routes and lanes data populated successfully!'))


    def populate_shipping_liners(self):
        liners_data = [
            {"name": "Maersk Line", "contact_details": "contact@maersk.com", "fleet_size": 700, "operational_area": "Global", "type_of_vessels": "Container Ships", "rating": 9},
            {"name": "MSC", "contact_details": "contact@msc.com", "fleet_size": 600, "operational_area": "Global", "type_of_vessels": "Bulk Carriers", "rating": 8},
            {"name": "CMA CGM", "contact_details": "contact@cma-cgm.com", "fleet_size": 500, "operational_area": "Global", "type_of_vessels": "Container Ships", "rating": 8},
            {"name": "Evergreen Marine", "contact_details": "contact@evergreen-marine.com", "fleet_size": 200, "operational_area": "Global", "type_of_vessels": "Container Ships", "rating": 7},
        ]

        for liner in liners_data:
            ShippingLiner.objects.get_or_create(**liner)
        self.stdout.write(self.style.SUCCESS('Shipping Liners data populated successfully!'))

    def populate_ships(self):
        liners = list(ShippingLiner.objects.all())
        ships_data = [
            # Maersk Line Ships (ID 1)
            {"name": "Ever Given", "registration_number": "EG12345", "ship_type": "Container Ship", "capacity": 20000, "flag": "Panama", "shipping_liner": liners[0]},
            {"name": "Maersk Alabama", "registration_number": "MA12346", "ship_type": "Container Ship", "capacity": 18000, "flag": "Denmark", "shipping_liner": liners[0]},
            {"name": "Maersk Emerald", "registration_number": "ME12347", "ship_type": "Container Ship", "capacity": 19000, "flag": "Denmark", "shipping_liner": liners[0]},
            {"name": "Maersk Heidelberg", "registration_number": "MH12348", "ship_type": "Container Ship", "capacity": 21000, "flag": "Denmark", "shipping_liner": liners[0]},
            
            # MSC Ships (ID 2)
            {"name": "MSC Oscar", "registration_number": "MSC98765", "ship_type": "Container Ship", "capacity": 19000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "MSC Zoe", "registration_number": "MSC98766", "ship_type": "Container Ship", "capacity": 18000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "MSC Ines", "registration_number": "MSC98767", "ship_type": "Container Ship", "capacity": 17000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "MSC Laila", "registration_number": "MSC98768", "ship_type": "Container Ship", "capacity": 16000, "flag": "Liberia", "shipping_liner": liners[1]},
            
            # CMA CGM Ships (ID 3)
            {"name": "CMA CGM Louis", "registration_number": "CGL12345", "ship_type": "Container Ship", "capacity": 20000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "CMA CGM Topaz", "registration_number": "CGL12346", "ship_type": "Container Ship", "capacity": 18000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "CMA CGM Marco Polo", "registration_number": "CGL12347", "ship_type": "Container Ship", "capacity": 19000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "CMA CGM Tigris", "registration_number": "CGL12348", "ship_type": "Container Ship", "capacity": 17000, "flag": "France", "shipping_liner": liners[2]},
            
            # Evergreen Marine Ships (ID 4)
            {"name": "Evergreen Eternal", "registration_number": "EE12345", "ship_type": "Container Ship", "capacity": 16000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "Evergreen Glory", "registration_number": "EG12346", "ship_type": "Container Ship", "capacity": 15000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "Evergreen Unity", "registration_number": "EU12345", "ship_type": "Container Ship", "capacity": 18000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "Evergreen Pride", "registration_number": "EP12345", "ship_type": "Container Ship", "capacity": 17000, "flag": "Taiwan", "shipping_liner": liners[3]},
            
            # Additional ships to complete 30 entries
            {"name": "CMA CGM Virginia", "registration_number": "CGL12349", "ship_type": "Container Ship", "capacity": 20000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "Maersk Harmony", "registration_number": "MH12349", "ship_type": "Container Ship", "capacity": 21000, "flag": "Denmark", "shipping_liner": liners[0]},
            {"name": "MSC Alina", "registration_number": "MSC98769", "ship_type": "Container Ship", "capacity": 19000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "MSC Isabella", "registration_number": "MSC98770", "ship_type": "Container Ship", "capacity": 18000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "CMA CGM Genesis", "registration_number": "CGL12350", "ship_type": "Container Ship", "capacity": 19000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "CMA CGM Beluga", "registration_number": "CGL12351", "ship_type": "Container Ship", "capacity": 18000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "Evergreen Phoenix", "registration_number": "EP12346", "ship_type": "Container Ship", "capacity": 16000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "Evergreen Freedom", "registration_number": "EF12345", "ship_type": "Container Ship", "capacity": 15000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "MSC Harmony", "registration_number": "MSC98771", "ship_type": "Container Ship", "capacity": 19000, "flag": "Liberia", "shipping_liner": liners[1]},
            {"name": "Maersk Progress", "registration_number": "MP12345", "ship_type": "Container Ship", "capacity": 20000, "flag": "Denmark", "shipping_liner": liners[0]},
            {"name": "Maersk Phoenix", "registration_number": "MP12346", "ship_type": "Container Ship", "capacity": 21000, "flag": "Denmark", "shipping_liner": liners[0]},
            {"name": "CMA CGM Fortune", "registration_number": "CGL12352", "ship_type": "Container Ship", "capacity": 18000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "CMA CGM Discovery", "registration_number": "CGL12353", "ship_type": "Container Ship", "capacity": 17000, "flag": "France", "shipping_liner": liners[2]},
            {"name": "Evergreen Star", "registration_number": "ES12345", "ship_type": "Container Ship", "capacity": 16000, "flag": "Taiwan", "shipping_liner": liners[3]},
            {"name": "Evergreen Brave", "registration_number": "EB12345", "ship_type": "Container Ship", "capacity": 15000, "flag": "Taiwan", "shipping_liner": liners[3]},
        ]
        for ship_data in ships_data:
            Ship.objects.get_or_create(**ship_data)
        self.stdout.write(self.style.SUCCESS('Ships data populated successfully!'))

 

    def populate_shipping_routes(self):
        routes = list(Route.objects.all())
        ships = list(Ship.objects.all())
        
        # Initialize an empty list to hold the routes data
        routes_data = []

        # Loop to generate 30 shipping routes
        for _ in range(50):
            route = random.choice(routes)
            ship = random.choice(ships)

            # Calculate departure and arrival schedules based on estimated duration
            departure_schedule = datetime.utcnow()
            arrival_schedule = departure_schedule + timedelta(days=route.estimated_duration)

            # Create the route entry
            route_entry = {
                "route": route,
                "ship": ship,
                "pricing_model": "per_teu",
                "departure_time": departure_schedule.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "arrival_time": arrival_schedule.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "liner_vessel_types": "Container Ships"
            }

            # Append the route entry to the list
            routes_data.append(route_entry)

        # Insert the route data into the database
        for route_data in routes_data:
            ShippingRoutes.objects.get_or_create(**route_data)

        # Success message
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
            {"username": "biswa","last_name": "ximble", "email": "biswa@ximble", "phone_number": "1234567891", "password": "ximble"},
            {"username": "anil", "last_name": "ximble","email": "anil@ximble", "phone_number": "1234567892", "password": "ximble"},
            {"username": "akash", "last_name": "ximble","email": "akash@ximble", "phone_number": "1234567893", "password": "ximble"},
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

    def create_booking(self):
        """Creates 5 bookings for each specified user."""
        usernames = ["anil", "biswa"]
        
        for username in usernames:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User {username} does not exist. Skipping..."))
                continue  # Skip to the next user if not found

            for _ in range(5):  # Create 5 bookings per user
                self.create_booking_for_user(user)

            self.stdout.write(self.style.SUCCESS(f"Successfully created 5 bookings for {username}."))




    def create_booking_for_user(self,user):
        """Creates a booking for user 'anil' with random cargo and route details."""
        user = user

        lane = Lane.objects.order_by('?').first()
        # Fetch routes by lane
        fetch_routes_by_lane = RouteLanes.objects.filter(lane=lane).values_list('route', flat=True)
        # Get serviceable routes
        serviceable_routes = list(ShippingRoutes.objects.filter(route__in=fetch_routes_by_lane))
        if not serviceable_routes:
            self.stdout.write(self.style.ERROR("No serviceable routes found."))
            return
        # Select a random shipping route
        shipping_route = random.choice(serviceable_routes)
        cargo = self.populate_cargo()

        STATUS_CHOICES = ['booked', 'in_transit', 'complete', 'cancelled']

        booking = Booking.objects.create(
            user=user,
            lane=lane,
            cargo=cargo,
            status=random.choice(STATUS_CHOICES),  # Random status selection
            shipping_route=shipping_route,
            total_price=random.uniform(5000, 50000)  # Random price between 5000 and 50000
        )

        # Possible tracking locations
        possible_locations = [
            "Port A - Shipment Departed",
            "Distribution Center - Processing",
            "Loading Dock - Awaiting Transport",
            "Cargo Hold - Secure",
            "Customs Clearance - In Progress"
        ]

        # Random remarks
        possible_remarks = [
            "Shipment is being processed.",
            "Loaded onto vessel.",
            "Awaiting clearance at customs.",
            "Cargo is secured and ready for transport.",
            "Preparing for departure."
        ]

        # Create initial tracking entry with randomized location and remarks
        tracking = Tracking.objects.create(
            status="in_transit",
            location=random.choice(possible_locations),  # Random initial location
            estimated_arrival=timezone.now() + timezone.timedelta(days=random.randint(3, 15)),  # Random ETA
            remarks=random.choice(possible_remarks),  # Random remark
        )

        booking.tracking = tracking
        booking.save()

        # Add at least two dummy documents
        document_types = [doc[0] for doc in Document.DOCUMENT_TYPE_CHOICES]  # Extract type keys
        for _ in range(2):  # Add at least 2 documents
            document_type = random.choice(document_types)
            document = Document.objects.create(
                booking=booking,
                document_type=document_type,
                document_url=f"https://example.com/documents/{uuid.uuid4()}.pdf",  # Dummy URL
                note="Auto-generated dummy document."
            )

        self.stdout.write(self.style.SUCCESS(f"Booking {booking.id} created for user {user.username}"))



    def populate_cargo(self):
        """Creates one random cargo and adds two random containers to it."""

        # Define possible cargo types
        CARGO_TYPES = ['fabrics', 'electronics', 'machinery', 'general', 'hazardous', 'refrigerated']
        IS_TEMPERATURE_CONTROLLED = [True, False]
        IS_DANGEROUS = [True, False]

        # Define possible container types
        CONTAINER_TYPES = [
            '20ft_standard', '40ft_standard', '20ft_reefer', '40ft_reefer',
            'flat_rack', 'open_top', 'tank', 'custom'
        ]
        USAGE_OPTIONS = [
            ['shipper_container'], 
            ['import_return'], 
            ['oversized'], 
            ['shipper_container', 'import_return'], 
            ['shipper_container', 'oversized']
        ]

        # Create a random cargo
        cargo = Cargo.objects.create(
            cargo_type=random.choice(CARGO_TYPES),
            is_temperature_controlled=random.choice(IS_TEMPERATURE_CONTROLLED),
            is_dangerous=random.choice(IS_DANGEROUS),
            description=f"Random description {random.randint(100, 999)}",
            earliest_departure_date=None  # Can be set dynamically if needed
        )

        # Create two random containers linked to the cargo
        for _ in range(2):
            Container.objects.create(
                cargo=cargo,
                container_type_size=random.choice(CONTAINER_TYPES),
                number_of_containers=random.randint(1, 10),
                weight_per_container=round(random.uniform(5.0, 30.0), 2),  # Weight in tons
                container_usage_options=random.choice(USAGE_OPTIONS)
            )

        return cargo