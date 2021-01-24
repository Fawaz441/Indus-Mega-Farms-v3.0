from django.urls import path
from .views import (add_item_to_cart,
remove_whole_from_cart,order_final,product_detail,products_list,
pay_now,add_product_review,ProdCatList
)


app_name = 'products'

urlpatterns = [
    path('',products_list,name='products'),
    path('product-category/<slug>',ProdCatList.as_view(),name='product_categories'),
    path('add_review',add_product_review,name='add_review'),                                                 #Products
    # path('well',stranger_products,name='stranger'),                                         #products for strangers
    path('<slug>/',product_detail,name='detail'),                                  #proposed detail view for products
    path('add_to_cart',add_item_to_cart,name='add_to_cart'),                         #adding a product to cart
    path('remove_whole_from_cart/<slug>',remove_whole_from_cart,name='remove_whole'),       #removing all instances of a product from cart
    path('order_final_summary',order_final,name='order_final'),                             #order summary(cart)
    path('pay_now',pay_now,name='pay_now',)                                                 #pay now
]

