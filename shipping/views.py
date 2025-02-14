from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.http import JsonResponse
from ports.models import Lane
from routes.models import  Route
from shipping.models import ShippingRoutes, Ship, ShippingLiner
from .serializers import ShipSerializer, ShippingLinerSerializer
from ocean_management_system.utils.response import custom_response

class ShipsByPortRoute(APIView):
    """
    Get available ships and shipping liners based on from_port_id and to_port_id.
    """

    def get(self, request):
        response = []
        status_code = 200
        message = "Ships and shipping liners fetched successfully."
        
        # Get from_port_id and to_port_id from request parameters
        from_port_id = request.GET.get('from_port_id')
        to_port_id = request.GET.get('to_port_id')

        if not from_port_id or not to_port_id:
            return custom_response(data=[], status=400, message="from_port_id and to_port_id are required.")

        try:
            # Raw SQL query
            query = """
                SELECT s2.name as shipping_liner_name, 
                s.name as ship_name,
                r.name as route_name, 
                r.total_distance as route_distance, 
                r.estimated_duration as route_time, 
                l.distance as lane_distance, 
                l.estimated_travel_time as lane_time,
                TO_CHAR((srr.departure_schedule->>0)::timestamp, 'YYYY-MM-DD HH24:MI:SS') as departure_schedule,
                TO_CHAR((srr.arrival_schedule->>0)::timestamp, 'YYYY-MM-DD HH24:MI:SS') as arrival_schedule,
                srr.pricing_model 
            FROM routes r
            JOIN routes_lanes_rel rlr ON rlr.route_id = r.id
            JOIN lanes l ON l.id = rlr.lane_id
            JOIN shipping_routes_rel srr ON srr.route_id = r.id
            JOIN ships s ON s.id = srr.ship_id
            JOIN shippingliners s2 ON s2.id = s.shipping_liner_id
            WHERE l.from_port_id = %s
            AND l.to_port_id = %s;
            """

            # Execute the query with parameters
            with connection.cursor() as cursor:
                cursor.execute(query, [from_port_id, to_port_id])
                rows = cursor.fetchall()

            # Get column names
            column_names = [desc[0] for desc in cursor.description]

            # Prepare the response data
            response = []
            for row in rows:
                row_data = {column_names[i]: row[i] for i in range(len(row))}
                response.append(row_data)

        except Exception as e:
            status_code = 500
            message = f"Error fetching data: {str(e)}"

        return custom_response(data=response, status=status_code, message=message)
