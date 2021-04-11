import random
from paystack.views import payment_verified
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from users.models import Student,Farmer,Company
from .models import Product,Order,OrderedProduct,Address,ProductReview,PRODUCT_CATEGORY
from .utils import add_to_cart_helper,check_quantity_in_cart,remove_single_from_cart_helper
from users.forms import DeliveryForm
from indus_mega_farms.utils import newsletter
from ads.models import Ad,AdCategory
from django.views.generic import ListView,View


def remove_single_item(request,code):
    return remove_single_from_cart_helper(request,code)


class ProdCatList(ListView):
    template_name = 'products2/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self,*args, **kwargs):
        return Product.objects.filter(category = self.kwargs['slug'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        categories = [i[0] for i in PRODUCT_CATEGORY]
        context['categories'] =  categories
        context['title'] = self.kwargs['slug']
        return context

def products_list(request):
    """
    View for the product list. Shows all the products available (ads inclusive)
    """
    category = request.GET.get('category')
    products = Product.objects.all().order_by('-created')
    if category:
        products = products.filter(category=category)
    categories = [i[0] for i in PRODUCT_CATEGORY]
    context = {
        'products':products,
        'title':'Products',
        'categories':categories
    }
    return render(request,'products2/product_list.html',context)



def product_detail(request,code):
    """
    Detail view for products. Shows product price, description and shows quantity of product in user's cart if already carted.
    """
    item = get_object_or_404(Product,code=code)
    similar_items = Product.objects.filter(category=item.category).exclude(id=item.id)
    count = similar_items.count()
    if(count >=5 ):
        similar_items = random.sample(list(similar_items),5)
    else:
        similar_items = random.sample(list(similar_items),count)
    title = item.name
    context = {'item':item,"title":title,'similar_items':similar_items}
    item_ad = Ad.objects.filter(product=item)
    if request.user.is_authenticated:
        context['in_cart'] = check_quantity_in_cart(request,item) > 0
    else:
        context['in_cart'] = False
    is_ad = False
    if item_ad.exists():
        the_ad = item_ad.first()
        is_ad = True
        if the_ad.ending_date <= timezone.now():
            item.delete()
            messages.error(request,'That product is no longer available')
            return redirect('home')
        else:
            if request.user != the_ad.seller.user:
                the_ad.view += 1
                the_ad.save()
            context["is_ad"] = is_ad
            context["ad"] = item_ad[0]
    return render(request,'products2/product_detail.html',context=context)
    


class AddItemToCart(View,LoginRequiredMixin):
    def get(self,request,code):
        if not request.user.is_authenticated:
            messages.error(request,'You are not logged in')
            return redirect('users:login')
        newsletter(request)
        product = get_object_or_404(Product,code=code)
        carted_prod,created = OrderedProduct.objects.get_or_create(item=product,user=request.user,ordered=False)
        return add_to_cart_helper(request,product,carted_prod)
    

@login_required
def remove_whole_from_cart(request,code):
    """View to remove an instance of an item from user cart."""
    newsletter(request)
    login_redirect_url = 'users:login'
    product = get_object_or_404(Product,code=code)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__code=code).exists():
            order_item = order.order_items.filter(item__code=code)[0]
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
    if name ==  '':
        name = 'Unknown'
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
    if 'ad_category' in request.session.keys():
        category = request.session["ad_category"]
        print(category)
        ad_category = AdCategory.objects.get(name=category)
        ads = Ad.objects.filter(ad_category=ad_category,seller=request.user.seller)
        for ad in ads.all():
            print(ad)
            ad.active = True
            ad.paid = True
            if not ad.product:
                product = Product.objects.create(
                    name = ad.name_of_product,
                    price = ad.minimum_price,
                    image = ad.sample_of_product,
                    description = ad.description,
                    category = ad.category
                )
                ad.product = product
            ad.save()
        del request.session["ad_category"]
        messages.info(request,"Payment successful")
        return redirect('users:user_home')

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


