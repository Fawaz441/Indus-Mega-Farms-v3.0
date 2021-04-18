import random
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def checkExistenceOfCode(code):
    return Product.objects.filter(code=code).exists()


def generate_product_code():
    code = ''
    for x in range(16):
        code += str(random.randrange(9))
    if checkExistenceOfCode(code):
        return generate_product_code()
    return code
# Create your models here.


PRODUCT_CATEGORY = (
    ("PROCESSED_FOOD", "PROCESSED_FOOD"),
    ("CROPS", "CROPS"),
    ("FRUITS", "FRUITS"),
    ("LIVESTOCK", "LIVESTOCK"),
    ("STUDENT_ITEMS", "STUDENT_ITEMS"),
    ("FARM_TOOLS", "FARM_TOOLS"),
    ("FARM_MACHINERY", "FARM_MACHINERY"),
    ("FARM_SERVICES", "FARM_SERVICES"),
    ("FOOD_STUFF", "FOOD_STUFF"),
    ("LAND", "LAND"),
    ("OTHER", "OTHER")
)


# Company Orders(special)
class CompanyOrder(models.Model):
    quality = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    location_of_delivery = models.CharField(max_length=1000)
    total_price = models.FloatField()
    expected_delivery_date = models.DateField()


# Product
class Product(models.Model):
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=1000, null=True, blank=True)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=40, choices=PRODUCT_CATEGORY)
    is_ad = models.BooleanField(default=False)
    ad_payment_settled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def detail(self):
        return reverse('products:detail', kwargs={'slug': self.code})

    def get_price(self):
        return self.price

    @property
    def image(self):
        if ProductImage.objects.filter(product=self).exists():
            return ProductImage.objects.filter(product=self).first().image
        return None

    @property
    def images(self):
        if ProductImage.objects.filter(product=self).exists():
            return ProductImage.objects.filter(product=self)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)


# Ordered Products
class OrderedProduct(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='in_cart')  # remember to set null#
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def get_normal_total_price(self):
        if self.item is not None:
            return self.item.price * self.quantity
        else:
            return 0

    def get_final_price(self):
        return self.get_normal_total_price()

    def str(self):
        return "{} of {}".format(self.quantity, self.item.name)

# Orders


class Order(models.Model):
    order_items = models.ManyToManyField(OrderedProduct)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivered = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    im_reference_code = models.CharField(max_length=20, null=True, blank=True)
    amount_paid = models.CharField(max_length=400, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    paystack_reference_code = models.CharField(
        null=True, blank=True, max_length=100)
    delivery_location = models.CharField(max_length=200, null=True, blank=True)
    time_left = models.IntegerField(default=50)
    pay_on_delivery = models.BooleanField(default=False)

    def get_total_order_price(self):
        total = 0
        for item in self.order_items.all():
            total += item.get_final_price()
        return total

    @property
    def get_products(self):
        content = ''
        for item in self.order_items.all():
            content += '{}({}), '.format(item.item.name,item.quantity)
        return content

    def str(self):
        return self.user.username

# Address for deliveries


class Address(models.Model):
    address = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'


class ProductReview(models.Model):
    review = models.TextField()
    user = models.CharField(max_length=10)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)


def assign_code(sender, instance, created, **kwargs):
    if created:
        instance.code = generate_product_code()
        instance.save()


post_save.connect(assign_code, sender=Product)
