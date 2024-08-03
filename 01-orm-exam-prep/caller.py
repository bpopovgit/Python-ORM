import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F


# Import your models here

# Create queries within functions

def get_profiles(search_string=None):
    if search_string:
        profiles = Profile.objects.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
        ).order_by('full_name').annotate(num_of_orders=Count('order'))
    else:
        profiles = Profile.objects.all().order_by('full_name').annotate(num_of_orders=Count('order'))

    if not profiles:
        return ""

    result = ""
    for profile in profiles:
        result += f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {profile.num_of_orders}\n"

    return result.strip()  # Remove the trailing newline character


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    result = ""
    for profile in profiles:
        result += f"Profile: {profile.full_name}, orders: {profile.order_count}\n"

    return result.strip()  # Remove the trailing newline character


def get_last_sold_products():
    last_order = Order.objects.order_by('-creation_date').first()

    if not last_order:
        return ""

    products = last_order.products.order_by('name')
    product_names = [product.name for product in products]

    return "Last sold products: " + ", ".join(product_names) if product_names else ""


def get_top_products():
    products = Product.objects.annotate(
        num_orders=Count('order')
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-num_orders', 'name'
    )[:5]

    if not products.exists():
        return ""

    result = "Top products:\n"
    for product in products:
        result += f"{product.name}, sold {product.num_orders} times\n"

    return result.strip()  # Remove the trailing newline character


def apply_discounts():
    orders = Order.objects.annotate(num_products=Count('products')).filter(num_products__gt=2, is_completed=False)
    num_of_updated_orders = orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"
