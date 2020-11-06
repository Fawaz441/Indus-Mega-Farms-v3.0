from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class ExactLockdownEntries(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15,default='',null=True)
    seen = models.BooleanField(default=False,null=True,blank=True)
    slides = models.FileField(upload_to='lockdown_entries')
    created_date = models.DateTimeField(auto_now_add=True)