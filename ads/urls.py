from django.urls import path
from .views import ad_categories_view,ad_category_detail,create_ad,sponsoredAds
app_name = 'ads'

urlpatterns = [
    path('',ad_categories_view,name='index'),
    path('<name>',ad_category_detail,name='ad_cat_detail'),
    path('create_ad/',create_ad,name='ad_create'),
    path('sponsored_ads/',sponsoredAds,name='sponsored_ads')
]