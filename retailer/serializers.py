from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import Retailer, Orders
from distributor.models import Distributor, OrdersAccepted
from user.serializers import ProfileSerializer, ProductSerializer


class OrdersSerializer(ModelSerializer):
    accepted_by = SerializerMethodField()
    location = CharField(source = 'route.location')
    retailer = SerializerMethodField()
    product = SerializerMethodField()
    class Meta:
        model = Orders
        fields = ['id', 'status', 'product', 'retailer', 'required', 'location', 'accepted_by']
        
    def get_accepted_by(self, obj):
        if (obj.status == 'ACCEPTED' or obj.status == 'REJECTED'):
            order = OrdersAccepted.objects.filter(order=obj).first()
            if order:
                return ProfileSerializer(order.distributor).data
        return None
    
    def get_retailer(self, obj):
        return ProfileSerializer(obj.retailer).data
    
    def get_product(self, obj):
        return ProductSerializer(obj.product).data