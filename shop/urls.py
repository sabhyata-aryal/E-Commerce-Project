from django.urls import path
from . import views

urlpatterns = [
    path('liquor/', views.liquor_index, name='liquor_index'),
    path('liquor/<slug:slug>/', views.products_by_subcategory, name='liquor_subcategory'),
    path('', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('meat/', views.meat_shop, name='meat_shop'),
    path('meat/<slug:slug>/', views.meat_subcategory, name='meat_subcategory'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('restaurant/', views.restaurant_menu, name='restaurant'),

]
