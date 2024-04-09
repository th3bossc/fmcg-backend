app_name = 'distributor'

from django.urls import path
from .views import DistributorView, DistributorDetailView, DistributorReceiptsView, DistributorDemandView
urlpatterns = [
    path("", DistributorView.as_view(), name="retailers"),
    path("<int:pk>/", DistributorDetailView.as_view(), name="retailer"),
    path("receipts/", DistributorReceiptsView.as_view(), name="retailer_orders"),
    path("demand/", DistributorDemandView.as_view(), name="retailer_orders"),
]