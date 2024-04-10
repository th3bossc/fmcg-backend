from rest_framework.serializers import ModelSerializer, CharField
from .models import UserAccount, Notification, Route, Product

class ProfileSerializer(ModelSerializer):
    role = CharField(source = 'type')
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'role', 'contact', 'address']
        
        
        
class NotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'day'] 
        
        
class RoutesSerializer(ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'routeName', 'text', 'source', 'destination', 'location'] 
        
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'brand', 'demand', 'priority']