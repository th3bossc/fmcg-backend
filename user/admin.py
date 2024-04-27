from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, Notification, Route, Product
from django.contrib.admin import ModelAdmin
# Register your models here.

class UserAdminConfig(UserAdmin):
    model = UserAccount
    search_fields = ('email', 'name', 'contact')
    list_filter = ('email', 'contact', 'is_active', 'is_staff', 'type')
    list_display = ('email', 'name', 'contact', 'is_active', 'is_staff', 'type')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'contact', 'address', 'password', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions')},),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'contact', 'address', 'password1', 'password2', 'is_active', 'is_staff', 'type')}
        ),
    )


class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'title', 'day')
    search_fields = ('user', 'title', 'day')
    fieldsets = (
        (None, {'fields': ('user', 'title', 'day')}),
    )
    list_filter = ('user', 'day')
    
class RouteAdmin(ModelAdmin):
    list_display = ('routeName', 'text', 'source', 'destination', 'cost')
    search_fields = ('routeName', 'text', 'source', 'destination', 'cost')
    fieldsets = (
        (None, {'fields': ('routeName', 'text', 'source', 'destination', 'cost')}),
    )
    list_filter = ('source', 'destination')
    
    
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'brand', 'demand', 'priority', 'price')
    search_fields = ('name', 'category', 'brand', 'demand', 'priority', 'price')
    fieldsets = (
        (None, {'fields': ('name', 'category', 'brand', 'demand', 'priority', 'price')}),
    )
    list_filter = ()


admin.site.register(UserAccount, UserAdminConfig)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Product, ProductAdmin)

