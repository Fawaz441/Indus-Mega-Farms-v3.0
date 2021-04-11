from products.models import Order,Product
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def add_to_cart_helper(request,product,carted_prod):
    """Helper function for adding an item to cart"""
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    carted_prod.quantity+=1
    carted_prod.save()
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__code=product.code).exists():
            order.order_items.add(carted_prod)
            messages.success(request,'You now have {} of {} in your IMcart'.format(carted_prod.quantity,carted_prod.item.name))
            return redirect('products:order_final')
        
        else:
            order.order_items.add(carted_prod)
            order.save()
            return redirect('products:order_final')
    
    else:
        order = Order.objects.create(user=request.user,ordered=False)
        order.order_items.add(carted_prod)
        messages.info(request,'This item has been added to your IMcart!')
        order.save()
        return redirect('products:products')


def check_quantity_in_cart(request,item):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__code=item.code).exists():
            order_item = order.order_items.filter(item__code=item.code)[0]
            in_cart_quantity = order_item.quantity
            return in_cart_quantity
        else:
            return 0
    else:
        return 0



def remove_single_from_cart_helper(request,code):
    """Helper function for adding an item to cart"""
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    product = Product.objects.get(code=code)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__code=product.code).exists():
            carted_prod = order.order_items.filter(item__code=product.code)[0]
            carted_prod.quantity-=1
            carted_prod.save()
            if carted_prod.quantity == 0:
                carted_prod.delete()
            return redirect('products:order_final')
    else:
        messages.error(request,'Error!')
        return redirect('products:products')
        