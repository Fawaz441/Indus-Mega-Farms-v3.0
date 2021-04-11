from django.urls import path
from .views import ad_categories_view,AdDetailCreate,ad_category_detail,create_ad,Ads
app_name = 'ads'

urlpatterns = [
    path('',ad_categories_view,name='index'),
    path('<name>',ad_category_detail,name='ad_cat_detail'),
    path('create_ad/',create_ad,name='ad_create'),
    path('ads/',Ads,name='sponsored_ads'),
    path('create-details/',AdDetailCreate.as_view(),name='ad_details_create')
]