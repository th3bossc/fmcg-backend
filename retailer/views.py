from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Retailer, Orders
from .serializers import OrdersSerializer
from user.serializers import ProfileSerializer
from rest_framework.exceptions import NotFound

class RetailerView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        retailers = Retailer.objects.all()
        serialized_retailers = ProfileSerializer(retailers, many=True)
        return Response(serialized_retailers.data)
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        contact = request.data.get('contact')
        address = request.data.get('address') or "Address not provided"
        
        if not email or not password or not name or not contact:
            raise NotFound(detail="Please provide all required fields")
        
        try:
            retailer = Retailer.objects.create(email=email, name=name, contact=contact, address=address)
            retailer.set_password(password)
            retailer.save()
            serialized_retailer = ProfileSerializer(retailer)
            return Response(serialized_retailer.data)
        except Exception as e:
            raise NotFound(detail="Retailer not created")
        
        


class RetailerDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            retailer = Retailer.objects.get(id=pk)
            serialized_retailer = ProfileSerializer(retailer)
            return Response(serialized_retailer.data)
        except Exception as e:
            raise NotFound(detail="Retailer not found")


class RetailerOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if (request.user.type != 'RETAILER'):
            raise NotFound(detail="User is not a retailer")
        try:
            orders = Orders.objects.filter(retailer=request.user)
            serialized_orders = OrdersSerializer(orders, many=True)
            return Response(serialized_orders.data)
        except Exception as e:
            print(e)
            raise NotFound(detail="User not found")