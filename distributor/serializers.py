from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import Distributor, OrdersAccepted
from retailer.models import Orders
from user.serializers import ProductSerializer, ProfileSerializer

        
    
class OrdersAcceptedSerializer(ModelSerializer):
    product = SerializerMethodField()
    retailer = SerializerMethodField()
    class Meta:
        model = OrdersAccepted
        fields = ['id', 'product', 'retailer', 'accepted']
        
    def get_retailer(self, obj):
        return ProfileSerializer(obj.order.retailer).data
    
    def get_product(self, obj):
        return ProductSerializer(obj.order.product).data
    
class DemandSerializer(ModelSerializer):
    product = SerializerMethodField()
    location = CharField(source = 'route.location')
    retailer = SerializerMethodField()
    class Meta:
        model = Orders
        fields = ['id', 'product', 'retailer', 'required', 'location']
        
    def get_product(self, obj):
        return ProductSerializer(obj.product).data
    
    def get_retailer(self, obj):
        return ProfileSerializer(obj.retailer).data