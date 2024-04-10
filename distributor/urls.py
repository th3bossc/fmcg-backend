app_name = 'distributor'

from django.urls import path
from .views import DistributorView, DistributorDetailView, DistributorReceiptsView, DistributorDemandView, AcceptHandler, RejectHandler
urlpatterns = [
    path("", DistributorView.as_view(), name="retailers"),
    path("<int:pk>/", DistributorDetailView.as_view(), name="retailer"),
    path("receipts/", DistributorReceiptsView.as_view(), name="retailer_orders"),
    path("demand/", DistributorDemandView.as_view(), name="retailer_orders"),
    path("demand/accept/<str:pk>/", AcceptHandler.as_view(), name="accept_order"),
    path("demand/reject/<str:pk>/", RejectHandler.as_view(), name="reject_order"),
]