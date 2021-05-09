from django.urls import path
from .views import (AddItemToCart,
remove_whole_from_cart,order_final,product_detail,ProductList,
pay_now,add_product_review,ProdCatList,remove_single_item
)


app_name = 'products'

urlpatterns = [
    path('',ProductList.as_view(),name='products'),
    path('product-category/<slug>',ProdCatList.as_view(),name='product_categories'),
    path('add_review',add_product_review,name='add_review'),                                                 #Products
    # path('well',stranger_products,name='stranger'),                                         #products for strangers
    path('<code>/',product_detail,name='detail'),                                  #proposed detail view for products
    path('remove_single/<code>',remove_single_item,name='remove_single'),                         #adding a product to cart
    path('add_to_cart/<code>',AddItemToCart.as_view(),name='add_to_cart'),                         #adding a product to cart
    path('remove_whole_from_cart/<code>',remove_whole_from_cart,name='remove_whole'),       #removing all instances of a product from cart
    path('order_final_summary',order_final,name='order_final'),                             #order summary(cart)
    path('pay_now',pay_now,name='pay_now',)                                                 #pay now
]

