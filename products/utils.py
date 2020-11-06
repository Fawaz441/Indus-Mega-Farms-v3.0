from products.models import Order
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def add_to_cart_helper(request,product,carted_prod,quantity):
    """Helper function for adding an item to cart"""
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__slug=product.slug).exists():
            carted_prod.quantity  = quantity
            carted_prod.save()
            order.order_items.add(carted_prod)
            messages.success(request,'You now have {} of {} in your IMcart'.format(carted_prod.quantity,carted_prod.item.name))
            return redirect('products:order_final')
        
        else:
            order.order_items.add(carted_prod)
            carted_prod.quantity = quantity
            carted_prod.save()
            order.save()
            return redirect('products:order_final')
    
    else:
        order = Order.objects.create(user=request.user,ordered=False)
        carted_prod.quantity=quantity
        carted_prod.save()
        order.order_items.add(carted_prod)
        messages.info(request,'This item has been added to your IMcart!')
        order.save()
        return redirect('products:products')


def check_quantity_in_cart(request,item):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__slug=item.slug).exists():
            order_item = order.order_items.filter(item__slug=item.slug)[0]
            in_cart_quantity = order_item.quantity
            return in_cart_quantity
        else:
            return 0
    else:
        return 0