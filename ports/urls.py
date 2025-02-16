from django.urls import path
from .views import PortList, PortDetail, check_lane_availability

urlpatterns = [
    path('ports/', PortList.as_view(), name='port-list'),
    path('ports/<int:id>/', PortDetail.as_view(), name='port-detail'),

    path('check-availabe-lanes/', check_lane_availability, name='check_lane_availability'),


]
