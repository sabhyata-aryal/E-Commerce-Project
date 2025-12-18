from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),

    # Khalti
    path('khalti/initiate/', views.khalti_initiate, name='khalti_initiate'),
    path('khalti/callback/', views.khalti_callback, name='khalti_callback'),

    path('success/', views.order_success, name='order_success'),
]
