from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView,DetailView
from django.contrib import messages
from django.db.models.aggregates import Sum
from django.contrib.auth.models import User
from products.models import PRODUCT_CATEGORY, Product, ProductImage, Order
from ads.models import Seller, Ad, AdCategory
from django.utils import timezone
from .mixins import IsAdminMixin
from django.db.models import Q

MONTHS = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

class AdminView(IsAdminMixin, View):
    def get(self, request):
        ads = Ad.objects.filter(ending_date__gte=timezone.now()).prefetch_related('seller','ad_category','product')
        pending_orders_list = Order.objects.filter(ordered=True,delivered=False)
        pending_orders = pending_orders_list.count()
        context = {'pending_orders_list': pending_orders_list,
                   'pending_orders': pending_orders,
                   'ads':ads,'title':'Overview'}
        return render(request, 'administration/index.html', context)


class AllOrders(IsAdminMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        count = orders.count()
        context = {'orders': orders, 'count': count,'title':'All Orders'}
        return render(request, 'administration/orders.html', context)


class AddProduct(IsAdminMixin, View):
    def get(self, request):
        categories = [i[0] for i in PRODUCT_CATEGORY]
        context = {'categories': categories,'title':'Create New Product'}
        return render(request, 'administration/add_product.html', context)

    def post(self, request):
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        new_product = Product.objects.create(
            name=name, price=float(price), category=category,
            description=description
        )

        for image in images:
            ProductImage.objects.create(image=image, product=new_product)
        messages.success(request, 'New product added successfully')
        return redirect(request.META['HTTP_REFERER'])


class NewAd(IsAdminMixin, View):
    def get(self, request):
        ad_categories = AdCategory.objects.all()
        sellers = Seller.objects.all()
        categories = [i[0] for i in PRODUCT_CATEGORY]
        context = {'categories': ad_categories,'title':'Create New Ad',
                   'sellers': sellers, 'product_categories': categories}
        return render(request, 'administration/new_ad.html', context)

    def post(self, request):
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        ad_category_id = request.POST.get('ad_category')
        prod_category = request.POST.get('prod_category')
        negotiable = request.POST.get('negotiable')
        seller = request.POST.get('seller')
        images = request.FILES.getlist('images')
        description = request.POST.get('description')

        new_product = Product.objects.create(
            name=product_name,
            price=float(product_price),
            description=description,
            category=prod_category,
            is_ad=True,
            ad_payment_settled=True
        )
        for image in images:
            ProductImage.objects.create(image=image, product=new_product)
        Ad.objects.create(
            ad_category=AdCategory.objects.get(id=ad_category_id),
            seller=Seller.objects.get(id=int(seller)),
            negotiable=(negotiable == 'on'),
            product=new_product
        )
        messages.success(request, 'Ad Created Successfully')
        return redirect(request.META('HTTP_REFERER'))


class CreateNewSeller(IsAdminMixin, View):
    def post(self, request):
        brand_name = request.POST.get('brand_name')
        seller_number = request.POST.get('seller_number')
        whatsapp_number = request.POST.get('whatsapp_number')
        location = request.POST.get('location')
        if Seller.objects.filter(brand_name__iexact=brand_name).exists():
            return JsonResponse({'message': 'Seller with this brand_name already exists'}, status=400)
        user = User.objects.create(username=brand_name)
        user.set_password('12345678')
        seller = Seller.objects.create(
            user=user,
            brand_name=brand_name,
            whatsapp_number=whatsapp_number,
            phone_number=seller_number,
            location=location
        )
        return JsonResponse({'brand_name': seller.brand_name, 'id': seller.id}, status=200)


class OrderChartView(IsAdminMixin,View):
    def get(self,request):
        now = timezone.now()
        current_year = now.year
        current_month = now.month

        orders = Order.objects.all()
        paid_orders = orders.filter(ordered=True)
        unpaid_orders = orders.filter(ordered=False)
        paid_orders_dict = {}
        unpaid_orders_dict = {}
        revenue_dict = {}

        for month in range(1,current_month+1):
            revenue = 0
            paid_orders_sum = paid_orders.filter(
                created_time__year=current_year,
                created_time__month=month
                )
            
            for order in paid_orders_sum:
                revenue+=int(order.amount_paid)
            revenue_dict.update({MONTHS[month]:revenue})
            paid_orders_sum = paid_orders_sum.count()
            paid_orders_dict.update({MONTHS[month]:paid_orders_sum})
            unpaid_orders_sum = unpaid_orders.filter(
                created_time__year=current_year,
                created_time__month=month
                ).count()
            unpaid_orders_dict.update({MONTHS[month]:unpaid_orders_sum})



        return JsonResponse({
            'paid':paid_orders_dict,
            'unpaid':unpaid_orders_dict,
            'revenue':revenue_dict
        })

        

class ProductListView(ListView):
    def get_queryset(self):
        q = self.request.GET.get('filter')
        if q:
            if q != '' and q != 'all':
                return Product.objects.filter(Q(name__icontains=q) | Q(category__icontains=q))
            if q == 'all':
                return Product.objects.all().order_by('category')
        return Product.objects.all().order_by('category')
    
    context_object_name = 'products'
    template_name = 'administration/products.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        return context


class DeleteExpiredAds(View):
    def get(self,request):
        ads = Ad.objects.filter(ending_date__lte=timezone.now())
        context = {'title':'Expired Ads','ads':ads}
        return render(request,'administration/expired_ads.html',context)

    def post(self,request):
        ads = Ad.objects.filter(ending_date__lte=timezone.now())
        for ad in ads:
            ad.product.delete()

        return redirect(request.META['HTTP_REFERER']) 


class DeleteProduct(IsAdminMixin,View):
    def get(self,request,code):
        product = Product.objects.get(code=code)
        name = product.name
        product.delete()
        messages.success(request, f'{name} deleted successfully')
        return redirect(request.META['HTTP_REFERER']) 


class ProductDetail(IsAdminMixin,View):
    def get(self,request,code):
        product = Product.objects.get(code=code)
        context = {
            'title':product.name,
            'product':product
        }
        return render(request,'administration/product_detail.html',context)

    def post(self,request,code):
        product = Product.objects.get(id=request.POST['product_id'])
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product,image=image)
        return redirect(request.META['HTTP_REFERER']) 

class DeleteProductImage(View):
    def get(self,request,id):
        product_image = ProductImage.objects.get(id=id)
        product_image.delete()
        return redirect(request.META['HTTP_REFERER']) 

        
def deliver_order(request,id):
    order = Order.objects.get(id=id)
    order.delivered=True
    order.save()
    return redirect(request.META['HTTP_REFERER']) 
