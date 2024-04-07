from django.db import models
from user.models import UserAccount

class DistributorManager(models.Manager): 
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