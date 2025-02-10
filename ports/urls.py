from django.urls import path
from .views import PortList, PortDetail

urlpatterns = [
    path('ports/', PortList.as_view(), name='port-list'),
    path('ports/<int:id>/', PortDetail.as_view(), name='port-detail'),
]
