from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import AdCategory,Seller,Ad,AdDetails
from .forms import SellerForm
from products.models import Product,ProductImage
from django.views.generic import ListView,View
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from utils.functions import generate_product_code
from django.conf import settings



# View for all the ad_categories
def ad_categories_view(request):
    ad_categories = AdCategory.objects.exclude(name='infinite')
    context = {
        'title':'Ads',
        'ad_categories':ad_categories,
    }
    return render(request,'ads/index.html',context)

@login_required
def ad_category_detail(request,name):
    request.session['ad_category'] = name
    login_redirect_url = 'users:login'
    form = SellerForm()
    seller_query = Seller.objects.filter(user=request.user)
    if seller_query.exists():
        is_seller = True
    else:
        is_seller = False
    ad_category = get_object_or_404(AdCategory,name=name)
    is_not_free = True
    if (name=='FREE'):
        is_not_free = False
    context = {
        'title':ad_category.name,
        'ad_category':ad_category,
        'is_seller':is_seller,
        'amount':str(int(ad_category.cost)),
        'email':request.user.email,
        'is_not_free':is_not_free
    }
    if Seller.objects.filter(user=request.user).exists():
        user_ads_items = Ad.objects.filter(ad_category=ad_category,seller=request.user.seller,paid=True)
        all_user_ads = Ad.objects.filter(ad_category=ad_category,seller=request.user.seller)
        context['all_user_ads'] = all_user_ads
        if user_ads_items.exists() or ad_category.name == 'Free Plan' :
            unpaid = False
            context['unpaid'] = False
        else:
            context['unpaid']  = True
            unpaid = True
    if request.method == 'POST':
        if 'details_to_start' in request.POST:
            print(request.POST)
            if not request.POST.get('phone_number').startswith('+'):
                messages.error(request,'Phone number must start with country code')
                return redirect(request.META['HTTP_REFERER'])
                
            if not request.POST.get('whatsapp_number').startswith('+'):
                messages.error(request,'Whatsapp number must start with country code')
                return redirect(request.META['HTTP_REFERER'])
            else:
                form = SellerForm(request.POST)
                if form.is_valid():
                    seller_form = form.save(commit=False)
                    seller_form.user = request.user
                    if is_seller:
                        messages.info(request,'You already have your seller info registered.')
                        return redirect(request.META['HTTP_REFERER'])
                    seller_form.save()
                    messages.info(request,'Seller info registered.')
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.info(request,'Error filling form.')
                    return redirect(request.META['HTTP_REFERER'])

    # if request.user in ad_category.users.all():
    try:
        user_ads = Ad.objects.filter(ad_category=ad_category,seller=request.user.seller)
        context['user_ads'] = user_ads[0]
        if user_ads.exists():
            context['category_user_ads_count'] = user_ads.count
    except:
        context['category_user_ads_count'] = 0

    context["form"] = form
    return render(request,'ads/detail.html',context)


def create_ad(request):
    if request.method == 'POST':
        product_category = request.POST.get('product_category')
        ad_category = request.POST.get('ad_category')
        product_name = request.POST.get('product_name')
        negotiable = request.POST.get('negotiable')
        fixed_price = request.POST.get('fixed_price')
        price = request.POST.get('price')
        images = request.FILES.getlist('product_images')
        description = request.POST.get('description')
        negotiable = (negotiable == 'on')
        new_product = Product.objects.create(
            name=product_name,
            price = price,
            description = description,
            category = product_category,
            is_ad = True
            )
        for image in images:
            ProductImage.objects.create(image=image,product=new_product)
        Ad.objects.create(
            ad_category = AdCategory.objects.get(name=ad_category),
            seller = request.user.seller,
            negotiable = negotiable,
            product = new_product
            )
        return redirect(request.META.get('HTTP_REFERER'))


def Ads(request):
    # paginator = Paginator(sup_ads, 25) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    parameter = request.GET.get("q")
    context = {
        # 'page_obj':page_obj,
        'title':'Indus-Mega Farms',
        'ADS_URL':settings.ADS_URL
    }
    failed = ''
    if parameter:
        if parameter != '':
            results = Product.objects.filter(name__icontains=parameter)
            if not results.exists():
                failed = "No products match your search."
        else:
            results = ''
        if request.is_ajax():
            html = render_to_string(
                template_name="ads/search_results.html", 
                context={"results": results,"failed":failed}
            )

            data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request,'ads/ads.html',context)
    


class AdDetailCreate(View):
    def post(self,request):
        ad_id = request.POST.get('ad_id')
        ad = Ad.objects.get(id=int(ad_id))
        labels = []
        values = []
        for i in request.POST:
            if i.startswith('label'):
                labels.append(request.POST[i])
            if i.startswith('value'):
                values.append(request.POST[i])
        for (label,value) in zip(labels,values):
            AdDetails.objects.create(ad=ad,label=label,value=value)
                


        return JsonResponse({},status=200)
