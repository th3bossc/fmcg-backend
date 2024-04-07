from django.urls import path
from .views import TestView, ProfileView

app_name = 'user'
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('profile/', ProfileView.as_view(), name='profile')
]