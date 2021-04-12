from django.urls import path
from .views import AdminView,AddProduct,NewAd

app_name = 'admn'

urlpatterns = [
    path('',AdminView.as_view(),name='home'),
    path('add-product',AddProduct.as_view(),name='add_product'),
    path('new-ad',NewAd.as_view(),name='new_ad')

]
