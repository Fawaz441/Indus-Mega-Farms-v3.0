from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from products.models import PRODUCT_CATEGORY,Product,ProductImage
from .mixins import IsAdminMixin


class AdminView(IsAdminMixin,View):
    def get(self, request):
        return render(request,'administration/index.html')

class AddProduct(IsAdminMixin,View):
    def get(self,request):
        categories = [i[0] for i in PRODUCT_CATEGORY]
        context = {'categories':categories}
        return render(request,'administration/add_product.html',context)

    def post(self,request):
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        new_product = Product.objects.create(
            name=name,price=float(price),category=category,
            description=description
        )

        for image in images:
            ProductImage.objects.create(image=image,product=new_product)
        messages.success(request,'New product added successfully')
        return redirect(request.META['HTTP_REFERER'])


class NewAd(IsAdminMixin,View):
    def get(self,request):
        return render(request,'administration/new_ad.html')
