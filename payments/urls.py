from django.urls import path
from . import views

urlpatterns = [
    path('esewa/', views.esewa_payment, name='esewa_payment'),
    path('esewa_success/', views.esewa_success, name='esewa_success'),
    path('esewa_failed/', views.esewa_failed, name='esewa_failed'),
]
