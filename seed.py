from django.contrib.auth import get_user_model
from catalog.models import Product


def run():
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(username="admin", email="admin@breadbreak.local", password="admin123", role="ADMIN")
    products = [
        {"name": "Sourdough Loaf", "description": "Crusty sourdough bread", "price_cents": 600},
        {"name": "Baguette", "description": "Classic French baguette", "price_cents": 350},
        {"name": "Croissant", "description": "Buttery flaky pastry", "price_cents": 300},
        {"name": "Cinnamon Roll", "description": "Sweet cinnamon swirl", "price_cents": 400},
    ]
    for p in products:
        Product.objects.get_or_create(name=p["name"], defaults=p)
