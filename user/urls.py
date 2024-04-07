from django.urls import path
from .views import TestView

app_name = 'user'
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
]