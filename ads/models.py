from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone
from products.models import Product
from django.conf import settings

#ad category
class AdCategory(models.Model):
    name = models.CharField(max_length=20)
    validity = models.CharField(max_length=10)
    no_of_ads = models.IntegerField()
    cost = models.FloatField()
    image = models.ImageField(upload_to='ad_categories',blank=True,null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)

    class Meta:
        verbose_name_plural = 'Ad Categories'
    
    def __str__(self):
        return self.name

# class Ad(models.Model):
    
    """Ad"""
class Ad(models.Model):
    ad_category = models.ForeignKey(AdCategory,related_name='ad_category',on_delete=models.SET_NULL,null=True)
    seller = models.ForeignKey('Seller',on_delete=models.CASCADE,related_name='seller_ads',null=True)
    negotiable = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    ending_date = models.DateTimeField(null=True,blank=True)
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE,related_name='prod_ad')
    view = models.IntegerField(default = 0)
    exhausted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return self.product.name
        return self.id

    @property
    def sample(self):
        return self.product.image


class AdDetails(models.Model):
    ad = models.ForeignKey(Ad,on_delete=models.CASCADE,related_name='details')
    label = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.label + ' : '+self.value
        
def set_ending_date(sender, instance, created, **kwargs):
    if created:
        duration = instance.ad_category.validity
        instance.ending_date = timezone.now() + timezone.timedelta(days=int(duration))
        instance.save()
post_save.connect(set_ending_date,sender=Ad)





# Seller account
class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='seller',on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username


