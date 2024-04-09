from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserAccount, Notification, Route
from .serializers import ProfileSerializer, NotificationsSerializer, RoutesSerializer
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        routes = Route.objects.all()
        serialized_routes = RoutesSerializer(routes, many=True)
        return Response(serialized_routes.data)