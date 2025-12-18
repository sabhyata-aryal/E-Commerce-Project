from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from shop import views  # import properly
from shop.models import Product


# Homepage view
def home(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True).order_by('-id')
    if not featured_products.exists():
        featured_products = Product.objects.filter(is_available=True).order_by('-id')[:3]
    return render(request, 'home.html', {'featured_products': featured_products})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # SHOP ROUTES
    path('shop/', include('shop.urls')),

    # RESTAURANT 
    path('restaurant/', views.restaurant_menu, name='restaurant'),

    # STAY PAGE 
    path('stay/', lambda request: render(request, 'stay.html'), name='stay'),

    # CART, ORDERS, PAYMENTS
    path('cart/', include('cart.urls')),
    path('orders/', include('customer_orders.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
