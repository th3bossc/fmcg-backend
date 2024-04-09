from django.db import models
from user.models import UserAccount, UserAccountManager

class DistributorManager(UserAccountManager): 
    def create_user(self, email, name, contact, address, password, **other_fields): 
        if not email or len(email) <= 0:  
            raise  ValueError("Email field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
          
        user = self.model( 
            email = self.normalize_email(email),
            name = name,
            contact = contact,
            address = address,
            **other_fields  
        ) 
        user.set_password(password) 
        user.save() 
        return user 
    
    
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(type = UserAccount.Types.DISTRIBUTOR) 
        return queryset  
        
class Distributor(UserAccount): 
    class Meta :  
        proxy = True
    objects = DistributorManager()
      
    def save(self , *args , **kwargs):
        if not self.id or self.id == None: 
            self.type = UserAccount.Types.DISTRIBUTOR 
        self.is_distributor = True
        return super().save(*args , **kwargs)
    
    
class OrdersAccepted(models.Model):
    distributor = models.ForeignKey(Distributor , on_delete = models.CASCADE)
    order = models.ForeignKey('retailer.Orders' , on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)
    
    def accept(self, *args, **kwargs):
        self.order.status = 'ACCEPTED'
        self.order.save()
        self.accepted = True
        return super().save(*args, **kwargs)
    
    def reject(self, *args, **kwargs):
        self.order.status = 'REJECTED'
        self.order.save()
        self.accepted = False
        return super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if (self.accepted):
            self.order.status = 'ACCEPTED'
        else:
            self.order.status = 'REJECTED'
        self.order.save()
        return super().save(*args, **kwargs)