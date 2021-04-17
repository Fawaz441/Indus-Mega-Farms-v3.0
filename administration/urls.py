from django.urls import path
from .views import AdminView, AddProduct, NewAd, AllOrders, CreateNewSeller

app_name = 'admn'

urlpatterns = [
    path('', AdminView.as_view(), name='home'),
    path('add-product', AddProduct.as_view(), name='add_product'),
    path('all-orders', AllOrders.as_view(), name='all_orders'),
    path('new-ad', NewAd.as_view(), name='new_ad'),
    path('create-seller', CreateNewSeller.as_view(), name='create_seller')

]
