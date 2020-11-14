from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

PRODUCT_CATEGORY = (
    ("PROCESSED_FOOD","PROCESSED_FOOD"),
    ("CROPS","CROPS"),
    ("FRUITS","FRUITS"),
    ("LIVESTOCK","LIVESTOCK"),
    ("STUDENT_ITEMS","STUDENT_ITEMS"),
    ("FARM_TOOLS","FARM_TOOLS"),
    ("FARM_MACHINERY","FARM_MACHINERY"),
    ("FARM_SERVICES","FARM_SERVICES"),
    ("FOOD_STUFF","FOOD_STUFF"),
    ("LAND","LAND"),
    ("OTHER","OTHER")
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
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    slug = models.SlugField(blank=True,null=True,max_length=500)
    description = models.TextField()
    category = models.CharField(max_length=40,choices=PRODUCT_CATEGORY)
    image2 = models.ImageField(upload_to='products',blank=True,null=True)
    image3 = models.ImageField(upload_to='products',blank=True,null=True)
    image4 = models.ImageField(upload_to='products',blank=True,null=True)
    image5 = models.ImageField(upload_to='products',blank=True,null=True)
    image6 = models.ImageField(upload_to='products',blank=True,null=True)
    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def detail(self):
        return reverse('products:detail',kwargs={'slug':self.slug})

    def get_price(self):
        return self.price



# Ordered Products
class OrderedProduct(models.Model):
    item = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name='in_cart')  ##remember to set null#
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def get_normal_total_price(self):
        return self.item.price * self.quantity
    

    def get_final_price(self):
        return self.get_normal_total_price()

        
    def str(self):
        return "{} of {}".format(self.quantity,self.item.item)

# Orders
class Order(models.Model):
    order_items = models.ManyToManyField(OrderedProduct)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivered = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    im_reference_code = models.CharField(max_length=20,null=True,blank=True)
    amount_paid = models.CharField(max_length=400,null=True,blank=True)
    ordered=models.BooleanField(default=False)
    paystack_reference_code = models.CharField(null=True,blank=True,max_length=100)
    delivery_location = models.CharField(max_length=200,null=True,blank=True)
    time_left = models.IntegerField(default=50)
    pay_on_delivery = models.BooleanField(default=False)

    def get_total_order_price(self):
        total = 0
        for item in self.order_items.all():
            total+=item.get_final_price()
        return total


    def str(self):
        return self.user.username

# Address for deliveries
class Address(models.Model):
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User,related_name='address',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'


class ProductReview(models.Model):
    review = models.TextField()
    user = models.CharField(max_length=10)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews',null=True,blank=True)
   

