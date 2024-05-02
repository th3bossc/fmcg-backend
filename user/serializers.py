from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import UserAccount, Notification, Route, Product

class ProfileSerializer(ModelSerializer):
    role = CharField(source = 'type')
    address = SerializerMethodField()
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'role', 'contact', 'address']
        
        
    def get_address(self, obj):
        return obj.location.destination
        
        
        
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
        fields = ['id', 'name', 'category', 'brand', 'demand', 'priority', 'price']