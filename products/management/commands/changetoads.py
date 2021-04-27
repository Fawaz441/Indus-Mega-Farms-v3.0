from django.core.management.base import BaseCommand
from products.models import Product
from ads.models import Ad,AdCategory,Seller

class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        non_ad_products = Product.objects.filter(is_ad=False)
        for product in non_ad_products.all():
            product.is_ad = True
            product.save()
            Ad.objects.create(
                ad_category=AdCategory.objects.get(name='infinite'),
                seller=Seller.objects.get(user__username='arinzeFrank'),
                negotiable=True,
                product=product
            )
