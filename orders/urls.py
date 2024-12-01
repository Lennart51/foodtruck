from django.urls import path  # Import the 'path' function
from . import views  # Import views from the current directory

app_name = 'orders'  # Define the app name for URL namespacing

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # Define the URL pattern
]
