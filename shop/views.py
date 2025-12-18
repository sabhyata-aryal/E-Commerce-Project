from django.shortcuts import render, get_object_or_404
from .models import Category, SubCategory, Product

def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'shop/all_products.html', {
        'products': products,
        'categories': categories
    })


def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.get_all_products()
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'shop/products_by_category.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


# LIQUOR STORE
def liquor_index(request):
    liquor_cat = get_object_or_404(Category, slug='liquor')
    subcats = liquor_cat.subcategories_of_category.all().order_by('name')
    return render(request, 'shop/liquor_index.html', {
        'subcats': subcats,
        'liquor_cat': liquor_cat
    })


def products_by_subcategory(request, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    products = Product.objects.filter(subcategory=subcategory, is_available=True)
    main_category = subcategory.category.name.lower()

    if main_category == "liquor":
        template_name = 'shop/liquor_subcategory.html'
    else:
        template_name = 'shop/meat_subcategory.html'

    return render(request, template_name, {
        'subcategory': subcategory,
        'products': products,
    })


# MEAT SHOP
def meat_shop(request):
    category = get_object_or_404(Category, name__iexact="Meat")
    subcats = SubCategory.objects.filter(category=category)
    return render(request, 'shop/meat_shop.html', {
        'subcats': subcats
    })


def meat_subcategory(request, slug):
    subcat = get_object_or_404(SubCategory, slug=slug)
    products = Product.objects.filter(subcategory=subcat, is_available=True)
    return render(request, 'shop/meat_subcategory.html', {
        'subcategory': subcat,
        'products': products
    })



# RESTAURANT PAGE 
def restaurant_menu(request):
    # Get all restaurant subcategories (e.g. Breakfast, Lunch, Dinner)
    subcategories = SubCategory.objects.filter(category__name__iexact="Restaurant").order_by('name')
    
    # Check if user selected a specific subcategory via ?subcategory=slug
    selected_subcategory_slug = request.GET.get('subcategory')

    if selected_subcategory_slug:
        selected_subcategory = get_object_or_404(SubCategory, slug=selected_subcategory_slug)
        menu_items = Product.objects.filter(subcategory=selected_subcategory, is_available=True).order_by('name')
    else:
        selected_subcategory = None
        menu_items = Product.objects.filter(category__name__iexact="Restaurant", is_available=True).order_by('subcategory__name', 'name')

    return render(request, 'restaurant.html', {
        'subcategories': subcategories,
        'menu_items': menu_items,
        'selected_subcategory': selected_subcategory,
    })



