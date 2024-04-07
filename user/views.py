from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.


class TestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'Hello, World!'})
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'role': request.user.type,
            'contact': request.user.contact,
        })

