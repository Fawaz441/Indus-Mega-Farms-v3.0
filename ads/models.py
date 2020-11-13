from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone
from products.models import Product,PRODUCT_CATEGORY
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


class AdImage(models.Model):
    image = models.ImageField(upload_to='ads')
    ad = models.ForeignKey('Ad',related_name='ad_image',on_delete=models.CASCADE)

# class Ad(models.Model):
    
    """Ad"""
class Ad(models.Model):
    ad_category = models.ForeignKey(AdCategory,related_name='ad_category',on_delete=models.SET_NULL,null=True)
    seller = models.ForeignKey('Seller',on_delete=models.CASCADE,related_name='seller_ads',null=True)
    minimum_price = models.FloatField(null=True,blank=True)
    maximum_price = models.FloatField(null=True,blank=True)
    negotiable = models.BooleanField(default=False)
    sample_of_product = models.ImageField(upload_to='adverts')
    name_of_product = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    ending_date = models.DateTimeField(null=True,blank=True)
    category = models.CharField(choices=PRODUCT_CATEGORY,max_length=120)
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.SET_NULL)
    view = models.IntegerField(default = 0)
    fixed_price = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.name_of_product

        
def set_ending_date(sender, instance, created, **kwargs):
    if created:
        duration = instance.ad_category.validity
        if(duration == '180 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=180)
        elif(duration == '14 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=14)
        elif(duration == '7 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=7)
        elif(duration == '21 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=21)
        elif(duration == '31 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=31)
        elif(duration == '92 days'):
            instance.ending_date = instance.created_date + timezone.timedelta(days=92)
        instance.save()
post_save.connect(set_ending_date,sender=Ad)


# Seller account
class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='seller',on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username

class SponsoredAd(models.Model):
    seller = models.ForeignKey('Seller',on_delete=models.CASCADE,related_name='sponsored_ads',null=True)
    minimum_price = models.FloatField(null=True,blank=True)
    maximum_price = models.FloatField(null=True,blank=True)
    negotiable = models.BooleanField(default=False)
    image = models.ImageField(upload_to='adverts')
    image1 = models.ImageField(upload_to='adverts')
    image2 = models.ImageField(upload_to='adverts')
    image3 = models.ImageField(upload_to='adverts')
    image4 = models.ImageField(upload_to='adverts')
    image5 = models.ImageField(upload_to='adverts')
    image6 = models.ImageField(upload_to='adverts')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True,blank=True)
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.SET_NULL,related_name='sponsored_ad')
    view = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

