from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth.models import User
from products.models import PRODUCT_CATEGORY, Product, ProductImage, Order
from ads.models import Seller, Ad, AdCategory
from django.utils import timezone
from .mixins import IsAdminMixin
from django.db.models import Q


class AdminView(IsAdminMixin, View):
    def get(self, request):
        pending_orders_list = Order.objects.filter(
            ~Q(amount_paid=None) & Q(delivered=False))
        pending_orders = pending_orders_list.count()
        context = {'pending_orders_list': pending_orders_list,
                   'pending_orders': pending_orders}
        return render(request, 'administration/index.html', context)


class AllOrders(IsAdminMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        count = orders.count()
        context = {'orders': orders, 'count': count}
        return render(request, 'administration/orders.html', context)


class AddProduct(IsAdminMixin, View):
    def get(self, request):
        categories = [i[0] for i in PRODUCT_CATEGORY]
        context = {'categories': categories}
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
        context = {'categories': ad_categories,
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
        return redirect(request.META.get('HTTP_REFERER'))


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
