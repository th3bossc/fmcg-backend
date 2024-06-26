app_name = 'retailer'

from django.urls import path
from .views import RetailerView, RetailerDetailView, RetailerOrdersView, RetailerReceiptsView
urlpatterns = [
    path("", RetailerView.as_view(), name="retailers"),
    path("<int:pk>/", RetailerDetailView.as_view(), name="retailer"),
    path("orders/", RetailerOrdersView.as_view(), name="retailer_orders"),
    path('receipts/', RetailerReceiptsView.as_view(), name='retailer_receipts'),
]