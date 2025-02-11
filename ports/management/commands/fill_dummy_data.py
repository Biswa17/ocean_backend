from django.core.management.base import BaseCommand
from ports.models import Port, Lane
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Fill all tables with dummy data'

    def handle(self, *args, **kwargs):
        # Dummy Data for Ports
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

        # Creating Ports
        self.stdout.write(self.style.SUCCESS('Filling Ports data...'))
        for port in ports_data:
            Port.objects.create(**port)
        self.stdout.write(self.style.SUCCESS('Ports data populated successfully!'))

        # Dummy Data for Lanes
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

        # Create Lanes
        self.stdout.write(self.style.SUCCESS('Filling Lanes data...'))
        for lane in lanes_data:
            from_port = Port.objects.get(code=lane["from_port"])
            to_port = Port.objects.get(code=lane["to_port"])
            Lane.objects.create(
                from_port=from_port,
                to_port=to_port,
                distance=lane["distance"],
                estimated_travel_time=lane["estimated_travel_time"],
                lane_status=lane["lane_status"]
            )
        self.stdout.write(self.style.SUCCESS('Lanes data populated successfully!'))

        # Add more dummy data for other tables (Yards, ShippingLine, etc.)
        # For example, you can add Yards and other data similarly
        # Populate other models here if necessary

        self.stdout.write(self.style.SUCCESS('All tables populated with dummy data!'))
