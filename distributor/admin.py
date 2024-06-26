from django.contrib import admin
from .models import Distributor, OrdersAccepted
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
# Register your models here.



class UserAdminConfig(UserAdmin):
    model = Distributor
    search_fields = ('email', 'name', 'contact')
    list_filter = ('email', 'contact', 'is_active', 'type')
    list_display = ('email', 'name', 'contact', 'is_active')
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


class OrdersAcceptedAdmin(ModelAdmin):
    list_display = ('distributor', 'order', 'accepted')
    search_fields = ('distributor', 'order', 'accepted')
    list_filter = ('distributor', 'accepted')


admin.site.register(Distributor, UserAdminConfig)
admin.site.register(OrdersAccepted, OrdersAcceptedAdmin)