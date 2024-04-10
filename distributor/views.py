from rest_framework.views import APIView
from .models import Distributor, OrdersAccepted
from rest_framework.permissions import IsAuthenticated, AllowAny 
from retailer.models import Orders
from rest_framework.response import Response
from .serializers import OrdersAcceptedSerializer, DemandSerializer
from user.serializers import ProfileSerializer
from rest_framework.exceptions import NotFound

class DistributorView(APIView):
    def get(self, _):
        distributors = Distributor.objects.all()
        serialized_distributors = ProfileSerializer(distributors, many=True)
        return Response(serialized_distributors.data)
    
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        contact = request.data.get('contact')
        address = request.data.get('address') or "Address not provided"
        
        if not email or not password or not name or not contact:
            raise NotFound("Please provide all required fields")
        
        try:
            distributor = Distributor.objects.create(email=email, name=name, contact=contact, address=address)
            distributor.set_password(password)
            distributor.save()
            serialized_distributor = ProfileSerializer(distributor)
            return Response(serialized_distributor.data)
        except Exception as e:
            raise NotFound("Distributor not created")

class DistributorDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        distributor = Distributor.objects.get(id=pk)
        serialized_distributor = ProfileSerializer(distributor)
        return Response(serialized_distributor.data)    

class DistributorReceiptsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        distributor = request.user
        if distributor.type != 'DISTRIBUTOR':
            raise NotFound("User is not a distributor")
        try:
            orders = OrdersAccepted.objects.filter(distributor=distributor)
            serialized_orders = OrdersAcceptedSerializer(orders, many=True)
            return Response(serialized_orders.data)
        except Exception as e:
            raise NotFound("User not found")    

class DistributorDemandView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        orders = Orders.objects.filter(status="PENDING")
        serialized_orders = DemandSerializer(orders, many=True)
        return Response(serialized_orders.data)
    

class AcceptHandler(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        distributor = request.user
        if distributor.type != 'DISTRIBUTOR':
            raise NotFound("User is not a distributor")
        try:
            order = Orders.objects.get(id=pk)
            newOrder = OrdersAccepted.objects.create(order=order, distributor=distributor, accepted=True)
            newOrder.save()
            return Response({"message": "Order accepted"})
        except Exception as e:
            raise NotFound("Order not found")
        
        
class RejectHandler(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        distributor = request.user
        if distributor.type != 'DISTRIBUTOR':
            raise NotFound("User is not a distributor")
        try:
            order = Orders.objects.get(id=pk)
            newOrder = OrdersAccepted.objects.create(order=order, distributor=distributor, accepted=False)
            newOrder.save()
            return Response({"message": "Order rejected"})
        except Exception as e:
            raise NotFound("Order not found")