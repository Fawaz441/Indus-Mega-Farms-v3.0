from django.core.management.base import BaseCommand
from products.models import Product,generate_product_code

class Command(BaseCommand):

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            product.code = generate_product_code()
            product.save()        

            