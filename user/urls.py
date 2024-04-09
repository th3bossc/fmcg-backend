from django.urls import path
from .views import ProfileView, NotificationsView, RoutesView

app_name = 'user'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('routes/', RoutesView.as_view(), name='routes'),
]