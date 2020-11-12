from paystack.views import payment_verified
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models import Q

from users.models import Student,Farmer,Company
from .models import Product,Order,OrderedProduct,Address,ProductReview
from .utils import add_to_cart_helper,check_quantity_in_cart
from users.forms import DeliveryForm
from indus_mega_farms.utils import newsletter
from ads.models import Ad




def products_list(request):
    """
    View for the product list. Shows all the products available (ads inclusive)
    """
    total_products = Product.objects.count()
    try:
        processed_foods = Product.objects.filter(category='PROCESSED_FOOD')[:5]
    except:
        Product.objects.filter(category='PROCESSED_FOOD')
    try:
        crops = Product.objects.filter(category='CROPS')[:5]
    except:
        Product.objects.filter(category='CROPS')
    try:
        fruits = Product.objects.filter(category='FRUITS')[:5]
    except:
        fruits = Product.objects.filter(category='FRUITS')
    try:
        livestock = Product.objects.filter(category='LIVESTOCK')[:5]
    except:
        livestock = Product.objects.filter(category='LIVESTOCK')
    try:
        student_items = Product.objects.filter(category='STUDENT_ITEMS')[:5]
    except:
        student_items = Product.objects.filter(category='STUDENT_ITEMS')
    try:
        farm_tools = Product.objects.filter(category='FARM_TOOLS')[:5]
    except:
        farm_tools = Product.objects.filter(category='FARM_TOOLS')
    try:
        farm_machinery = Product.objects.filter(category='FARM_MACHINERY')[:5]
    except:
        farm_machinery = Product.objects.filter(category='FARM_MACHINERY')
    try:
        farm_services = Product.objects.filter(category='FARM_SERVICES')[:5]
    except:
        farm_services = Product.objects.filter(category='FARM_SERVICES')
    try:
        food_stuff = Product.objects.filter(category='FOOD_STUFF')[:5]
    except:
        food_stuff = Product.objects.filter(category='FOOD_STUFF')
    try:
        lands = Product.objects.filter(category='LAND')[:5]
    except:
        Product.objects.filter(category='LAND')
    context = {
        'processed_foods':processed_foods,
        'crops':crops,
        'fruits':fruits,
        'livestock':livestock,
        'student_items':student_items,
        'farm_tools':farm_tools,
        'farm_machinery':farm_machinery,
        'farm_services':farm_services,
        'food_stuff':food_stuff,
        'lands':lands,
        'total':total_products
    }
    return render(request,'products/product_list.html',context)



def product_detail(request,slug):
    """
    Detail view for products. Shows product price, description and shows quantity of product in user's cart if already carted.
    """
    item = get_object_or_404(Product,slug=slug)
    title = item.name
    context = {'item':item,"title":title}
    if request.user.is_authenticated:
        in_cart_quantity = check_quantity_in_cart(request,item)
        context["in_cart_quantity"] = in_cart_quantity
    item_ad = Ad.objects.filter(product=item)
    if item_ad.exists():
        the_ad = item_ad.first()
        if request.user != the_ad.seller.user:
            the_ad.view += 1
            the_ad.save()
        context["is_an_ad"] = True
        context["ad"] = item_ad[0]
    return render(request,'products/product_detail.html',context=context)
    

@require_POST
@csrf_exempt
def add_item_to_cart(request):
    """
    View to add an item to user cart.. User must be authenticated to access this view.
    """
    newsletter(request)
    login_url = 'users:login'
    slug = request.POST.get('slug')
    quantity = request.POST.get('quantity')
    product = get_object_or_404(Product,slug=slug)
    carted_prod,created = OrderedProduct.objects.get_or_create(item=product,user=request.user,ordered=False)
    add_to_cart_helper(request,product,carted_prod,quantity)
    return HttpResponse(status=200)
    

@login_required
def remove_whole_from_cart(request,slug):
    """View to remove an instance of an item from user cart."""
    newsletter(request)
    login_redirect_url = 'users:login'
    product = get_object_or_404(Product,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__slug=slug).exists():
            order_item = order.order_items.filter(item__slug=slug)[0]
            order.order_items.remove(order_item)
            messages.success(request,'You have successfully removed {} from your IMcart'.format(product.name))
            return redirect('products:order_final')
        else:
            messages.warning(request,'This item was never in your IMcart')
            return redirect('products:products')

    else:
        messages.warning(request,'You do not have an existing order!')
        return redirect('products:products')

def add_product_review(request):
    '''Add a product review'''
    slug = request.POST.get('product')
    product = Product.objects.filter(slug=request.POST.get('product'))[0]
    review = request.POST.get('review')
    name = request.POST.get('name')
    ProductReview.objects.create(
        review = review,
        user = name,
        product = product
    )
    messages.info(request,"Review added successfully")
    return redirect('products:detail',slug=slug)



@login_required
def order_final(request):
    """Pre - Payment view"""
    newsletter(request)
    current_order = Order.objects.filter(user=request.user,ordered=False)
    if current_order.exists():
        amount = current_order[0].get_total_order_price()
        current_order = current_order[0]
    else:
        messages.info(request,"No item in your cart")
        return redirect('home')

    form = DeliveryForm()
    title = "Cart"
    
    if request.method=="POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data.get("location")
            current_order.delivery_location = location
            for item in current_order.order_items.all():
                item.ordered=True
                item.save()
            current_order.save()
            return redirect("products:pay_now")
        else:
            print("form not valid")
    else:
        form = DeliveryForm()
    return render(request,'products/cart.html',{'current_order':current_order,'form':form})




#######################uncleared views##############333

@login_required 
@receiver(payment_verified)
def on_payment_received(request,sender,ref,amount,**kwargs):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    # if order_qs.exists() and (not 'gold' in request.session.keys()) and (not 'silver' in request.session.keys()) and (not 'company_sole' in request.session.keys()) and (not 'premium' in request.session.keys()):
    if order_qs.exists() and "order_payment" in request.session.keys():
        user_order = order_qs[0]
        user_order.paystack_reference_code = ref
        user_order.amount_paid = "N" + str(amount)
        user_order.ordered = True
        user_order.save()
        del request.session["order_payment"]
        messages.info(request,"Payment successful")
        return redirect('users:user_home')

    else:
        messages.warning(request,"No order!")
        return redirect('home')

@login_required
def pay_now(request):
    """Payment View"""
    request.session["order_payment"] = "order_payment"
    email = request.user.email
    current_order = Order.objects.filter(user=request.user,ordered=False,paystack_reference_code=None)
    if current_order.exists():
        amount = current_order[0].get_total_order_price()
        order = current_order[0]
        context = {
            'email':email,
            'amount':amount,
            'order':order
        }
        return render(request,'products/pay_now.html',context)
    else:
        messages.info(request,"You do not have an order")
        return redirect("users:user_home")


