from rest_framework.views import APIView
from .models import Distributor, OrdersAccepted
from rest_framework.permissions import IsAuthenticated, AllowAny 
from retailer.models import Orders
from rest_framework.response import Response
from .serializers import OrdersAcceptedSerializer, DemandSerializer
from user.serializers import ProfileSerializer

class DistributorView(APIView):
    def get(self, _):
        distributors = Distributor.objects.all()
        serialized_distributors = ProfileSerializer(distributors, many=True)
        return Response(serialized_distributors.data)

class DistributorDetailView(APIView):
    def get(self, request, pk):
        distributor = Distributor.objects.get(id=pk)
        serialized_distributor = ProfileSerializer(distributor)
        return Response(serialized_distributor.data)    

class DistributorReceiptsView(APIView):
    def get(self, request):
        distributor = request.user
        orders = OrdersAccepted.objects.filter(distributor=distributor)
        serialized_orders = OrdersAcceptedSerializer(orders, many=True)
        return Response(serialized_orders.data)    

class DistributorDemandView(APIView):
    def get(self, request):
        orders = Orders.objects.filter(status="PENDING")
        serialized_orders = DemandSerializer(orders, many=True)
        return Response(serialized_orders.data)
