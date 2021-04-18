from django.urls import path
from .views import (AdminView, AddProduct, NewAd, AllOrders, CreateNewSeller,
                    OrderChartView,ProductDetail,ProductListView,
                    DeleteExpiredAds,DeleteProduct,DeleteProductImage,deliver_order)

app_name = 'admn'

urlpatterns = [
    path('', AdminView.as_view(), name='home'),
    path('add-product', AddProduct.as_view(), name='add_product'),
    path('all-orders', AllOrders.as_view(), name='all_orders'),
    path('all-products', ProductListView.as_view(), name='all_products'),
    path('new-ad', NewAd.as_view(), name='new_ad'),
    path('create-seller', CreateNewSeller.as_view(), name='create_seller'),
    path('order-data',OrderChartView.as_view(),name='order_data'),
    path('expired-ads',DeleteExpiredAds.as_view(),name='expired_ads'),
    path('delete-product/<code>',DeleteProduct.as_view(),name='delete_product'),
    path('product-detail/<code>',ProductDetail.as_view(),name='product_detail'),
    path('del-prod-img/<id>',DeleteProductImage.as_view(),name='del_prod_img'),
    path('deliver-order/<id>',deliver_order,name='deliver_order'),

]
