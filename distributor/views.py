from rest_framework.views import APIView
from .models import Distributor, OrdersAccepted
from rest_framework.permissions import IsAuthenticated, AllowAny 
from retailer.models import Orders
from rest_framework.response import Response
from .serializers import OrdersAcceptedSerializer, DemandSerializer
from user.serializers import ProfileSerializer
from rest_framework.exceptions import NotFound
from datetime import datetime, timedelta
from user.models import Notification

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
    
    
    def post(self, request):
        if (request.user.type != 'DISTRIBUTOR'):
            raise NotFound("User is not a distributor")
        route = request.data.get('route')
        product = request.data.get('product')
        
        orders = OrdersAccepted.objects.filter(order__route=route, order__product=product, accepted=True, distributor=request.user)
        analysis_data = {
            "totalDemand": sum([order.order.required for order in orders]),
            "totalOrders": len(orders),
            "totalPrice": sum([order.order.product.price for order in orders]),
            "cost": orders[0].order.route.cost if len(orders) else 0,
        }
        
        return Response(analysis_data)  
    

class AcceptHandler(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        distributor = request.user
        if distributor.type != 'DISTRIBUTOR':
            raise NotFound("User is not a distributor")
        try:
            order = Orders.objects.get(id=pk)
            days = request.data.get('days')
            expectedDelivery = datetime.now() + timedelta(days=days)
            newOrder = OrdersAccepted.objects.create(order=order, distributor=distributor, accepted=True, expectedDeliveryTime=expectedDelivery)
            newOrder.save()
            
            orderedBy = order.retailer
            Notification.objects.create(user=orderedBy, message=f"Your order has been accepted by {distributor.name}")
            Notification.objects.create(user=orderedBy, message=f"Lead time for delivery is {days} days")
            
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
            retailer = order.retailer
            Notification.objects.create(user=retailer, message=f"Your order has been rejected by {distributor.name}")
            
            return Response({"message": "Order rejected"})
        except Exception as e:
            raise NotFound("Order not found")