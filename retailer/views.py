from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Retailer, Orders
from .serializers import OrdersSerializer
from user.serializers import ProfileSerializer
from rest_framework.exceptions import NotFound, bad_request
from distributor.models import OrdersAccepted
from distributor.serializers import OrdersAcceptedSerializer
from user.models import Product, Route

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
        location = request.data.get('address') or None
        
        if not email or not password or not name or not contact:
            raise NotFound(detail="Please provide all required fields")
        
        def get_first_obj():
            return Route.objects.first()
        
        try:
            if location is None:
                retailer = Retailer.objects.create(email=email, name=name, contact=contact, location=get_first_obj())
            else:
                retailer = Retailer.objects.create(email=email, name=name, contact=contact, location=location)
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
        
        
    def post(self, request):
        retailer = request.user
        if (retailer.type != 'RETAILER'):
            raise NotFound(detail="User is not a retailer")
        if not request.data['product'] or not request.data['required']:
            raise bad_request(detail="Please provide all required fields")
        product = Product.objects.get(pk=request.data.get('product'))
        route = retailer.location
        order = Orders.objects.filter(
            retailer=request.user,
            route=route,
            product=product,
            status='PENDING'
        ).first()
        if order:
            order.required += request.data.get('required')
        else:
            order = Orders.objects.create(
                retailer=request.user,
                product=product,
                required=request.data.get('required'),
                route=route
            )
        order.save()
        return Response(OrdersSerializer(Orders.objects.filter(retailer=request.user), many=True).data)
        
        
class RetailerReceiptsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        retailer = request.user
        if retailer.type != 'RETAILER':
            raise NotFound("User is not a retailer")
        try:
            orders = OrdersAccepted.objects.filter(order__retailer=retailer, accepted=True)
            serialized_orders = OrdersAcceptedSerializer(orders, many=True)
            return Response(serialized_orders.data)
        except Exception as e:
            raise NotFound("User not found")    
        
    def post(self, request):
        if request.user.type != 'RETAILER':
            raise NotFound("User is not a retailer")
        product = request.data.get('product')
        
        orders = OrdersAccepted.objects.filter(order__product=product, accepted=True, order__retailer=request.user.id)
        print(orders)

        analysis_data = {
            "totalDemand": sum([order.order.required for order in orders]),
            "totalOrders": len(orders),
            "totalPrice": sum([order.order.product.price for order in orders]),
            "cost": orders[0].order.route.cost if len(orders) else 0,
        }
        
        return Response(analysis_data) 