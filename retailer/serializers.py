from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import Retailer, Orders
from distributor.models import Distributor, OrdersAccepted
from user.serializers import ProfileSerializer


class OrdersSerializer(ModelSerializer):
    accepted_by = SerializerMethodField()
    location = CharField(source = 'route.location')
    class Meta:
        model = Orders
        fields = ['id', 'status', 'product', 'required', 'location', 'accepted_by']
        
    def get_accepted_by(self, obj):
        if (obj.status == 'ACCEPTED' or obj.status == 'REJECTED'):
            order = OrdersAccepted.objects.filter(order=obj).first()
            if order:
                return ProfileSerializer(order.distributor).data
        return None