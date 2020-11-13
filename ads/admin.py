from django.contrib import admin
from .models import Ad,AdCategory,AdImage,Seller,SponsoredAd

admin.site.register(SponsoredAd)
admin.site.register(Seller)
admin.site.register(Ad)
admin.site.register(AdCategory)
admin.site.register(AdImage)
