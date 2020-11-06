
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse

from pinax.referrals.models import Referral

# Create your models here.

class ProfilePictures(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='pic')
    profile_pic = models.ImageField(default='defaults/student.png',blank=True,null=True,upload_to='profile_images')

class ReferralCode(models.Model):
    code = models.OneToOneField(Referral,related_name='referral_intermediary',on_delete=models.CASCADE,blank=True, null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='code')
    referred = models.IntegerField(default=0)

class Student(models.Model):
    user = models.OneToOneField(User,related_name='student',on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return "{} {}".format(self.user.first_name,self.user.last_name) 

class Farmer(models.Model):
    user = models.OneToOneField(User,related_name='farmer',on_delete=models.CASCADE)
    land_size = models.CharField(max_length=20)
    other_products = models.CharField(max_length=1000,blank=True,null=True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=300)
    farm_name = models.CharField(max_length=200,null=True,blank=True)
    does_livestock = models.BooleanField(default=False,blank=True,null=True)
    major_products = models.CharField(max_length=200)
    is_subscribed = models.BooleanField(default=False)
    harvest_time = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)


    class Meta:
        verbose_name_plural = 'Farmers'

class Company(models.Model):
    user = models.OneToOneField(User,related_name='company',on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    is_seller = models.BooleanField(default=False)
    into_raw_materials = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)
 
    class Meta:
        verbose_name_plural = 'Companies'

    
class Challenger(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return "{}--{}".format(str(self.first_name),str(self.email)) 



class Complaint(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    attended_to = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class NewLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class SpecialMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='special_message')
    title = models.CharField(max_length=20,null=True,blank=True)
    message = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} to {} {}".format(self.message,self.user.first_name,self.user.last_name)


class Message(models.Model):
    title = models.CharField(max_length=20,null=True,blank=True)
    message = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)


# plans
# Plans
PLANS = (
    ("GOLD","GOLD"),
    ("SILVER","SILVER"),
    ("PREMIUM","PREMIUM")
)


class FarmerPlan(models.Model):
    subscribee = models.OneToOneField(Farmer,on_delete=models.CASCADE,related_name='plan',blank=True,null=True)
    category = models.CharField(choices=PLANS,max_length=7)
    customers = models.IntegerField(default=0)
    acheived =  models.BooleanField(default=False)

    def __str__(self):
        return "{}{} {}".format(self.subscribee.user.first_name,self.subscribee.user.last_name,str(self.customers))


class CompanySellerPlan(models.Model):
    subscribee = models.OneToOneField(Company,on_delete=models.CASCADE,related_name='plan',blank=True,null=True)
    patronages = models.IntegerField(default=0)
    acheived =  models.BooleanField(default=False)

    def __str__(self):
        return "{}{} {}".format(self.subscribee.user.first_name,self.subscribee.user.last_name,str(self.patronages))

class IMNews(models.Model):
    news = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.news
    class Meta:
        ordering = ['-created_date']

@receiver(post_save,sender=User)
def create_profile_pic(sender,instance,created,**kwargs):
    if created:
        ProfilePictures.objects.create(user=instance)


post_save.connect(create_profile_pic,sender=User)


