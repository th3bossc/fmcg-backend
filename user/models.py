from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin

# Create your models here.

class Route(models.Model):
    routeName=models.CharField(max_length=255)
    text=models.TextField()
    source=models.CharField(max_length=255)
    destination=models.CharField(max_length=255)
    cost=models.FloatField(default=30.0)
    
    
    @property
    def location(self):
        return f"{self.source} -> {self.destination}" 
class UserAccountManager(BaseUserManager): 
    def create_user(self, email, name, contact, password, **other_fields): 
        if not email or len(email) <= 0 :  
            raise  ValueError("Email field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
          
        user = self.model( 
            email = self.normalize_email(email),
            name = name,
            contact = contact,
            location = None,
            **other_fields  
        ) 
        user.set_password(password) 
        user.save() 
        return user 
      
    def create_superuser(self, email, name, contact, password, **other_fields): 
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, name, contact, password, **other_fields)
      


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        RETAILER = 'RETAILER', 'Retailer'
        DISTRIBUTOR = 'DISTRIBUTOR', 'Distributor'
    
    type = models.CharField(max_length=12, choices=Types.choices, default=Types.RETAILER)
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    location = models.ForeignKey(to='user.Route', on_delete=models.DO_NOTHING, null=True, blank=True) 
    
    is_active = models.BooleanField(default = True) 
    is_admin = models.BooleanField(default = False) 
    is_staff = models.BooleanField(default = False) 
    is_superuser = models.BooleanField(default = False) 
    
    is_retailer = models.BooleanField(default = False)
    is_distributor = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']
    
    objects = UserAccountManager()
    
    def __str__(self): 
        return str(self.email) 
      
    def has_perm(self , perm, obj = None): 
        return self.is_admin 
      
    def has_module_perms(self , app_label): 
        return True
      
    def save(self , *args , **kwargs): 
        if not self.type or self.type == None :  
            self.type = UserAccount.Types.RETAILER 
        return super().save(*args , **kwargs)
    

class Notification(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    day = models.DateTimeField()
    
    class Meta:
        ordering = ['-day']
        


    
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    demand = models.IntegerField()
    priority = models.IntegerField()
    price = models.FloatField(default=20.0)
    
    
    