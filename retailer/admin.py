from django.contrib import admin
from .models import Retailer, Orders
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
# Register your models here.



class UserAdminConfig(UserAdmin):
    model = Retailer
    search_fields = ('email', 'name', 'contact', 'location')
    list_filter = ('email', 'contact', 'location', 'is_active', 'type')
    list_display = ('email', 'name', 'contact', 'location', 'is_active')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'contact', 'location', 'password')}),
        ('Permissions', {'fields': ('is_active', 'user_permissions')},),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'contact', 'location', 'password1', 'password2', 'is_active')}
        ),
    )
    
class OrdersAdmin(ModelAdmin):
    list_display = ('retailer', 'product', 'status', 'required', 'route')
    search_fields = ('retailer', 'product', 'status', 'required', 'route')
    list_filter = ('retailer', 'status')
    


admin.site.register(Retailer, UserAdminConfig)
admin.site.register(Orders, OrdersAdmin)