from django.contrib import admin
from .models import Ad,AdCategory,Seller,AdDetails

admin.site.register(AdDetails)
admin.site.register(Seller)
admin.site.register(Ad)
admin.site.register(AdCategory)
