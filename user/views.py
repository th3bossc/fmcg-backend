from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserAccount, Notification, Route, Product
from .serializers import ProfileSerializer, NotificationsSerializer, RoutesSerializer, ProductSerializer
import random
# Create your views here.

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = ProfileSerializer(request.user)
        return Response(user.data)


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serialized_notifications = NotificationsSerializer(notifications, many=True)
        return Response(serialized_notifications.data)
    
    
class RoutesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        routes = Route.objects.all()
        serialized_routes = RoutesSerializer(routes, many=True)
        return Response(serialized_routes.data)
    
    
class ProductsView(APIView):
    permission_classes = [AllowAny]
    def get(self, _):
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)
    
    
    def post(self, request):
        product = ProductSerializer(data=request.data)
        product.demand = random.randint(10, 999)
        if product.is_valid():
            product.save()
            return Response(product.data)
        return Response(product.errors)
    