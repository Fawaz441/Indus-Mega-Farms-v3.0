from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import AdCategory,Seller,Ad,SponsoredAd
from .forms import SellerForm
from products.models import Product
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse


# View for all the ad_categories
def ad_categories_view(request):
    ad_categories = AdCategory.objects.all()
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
        has_seller = True
    else:
        has_seller = False
    ad_category = get_object_or_404(AdCategory,name=name)
    context = {
        'title':ad_category.name,
        'ad_category':ad_category,
        'has_seller':has_seller,
        'amount':str(int(ad_category.cost)),
        'email':request.user.email
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
            form = SellerForm(request.POST)
            seller_form = form.save(commit=False)
            seller_form.user = request.user
            if has_seller:
                messages.info(request,'You already have your seller info registered.')
                return redirect('users:user_home')
            seller_form.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            prod_category = request.POST.get('product_category')
            ad_category = request.POST.get('ad_category')
            product_name = request.POST.get('product_name')
            negotiable = request.POST.get('negotiable')
            fixed_price = request.POST.get('fixed_price')
            min_price = request.POST.get('minimum_price')
            max_price = request.POST.get('maximum_price')
            image = request.FILES.get('product_image')
            description = request.POST.get('description')
            ad_category = get_object_or_404(AdCategory,name=ad_category)
            ad_category.users.add(request.user)
            ad_category.save()
            if(negotiable == 'on'):
                negotiable = True
            else:
                negotiable = False
            if min_price == '':
                min_price = 0
            if max_price == '':
                max_price = 0
            if not unpaid or ad_category.name == 'Free Plan':
                ad = Ad.objects.create(
                ad_category = ad_category,
                seller = request.user.seller,
                minimum_price = min_price,
                maximum_price = max_price,
                sample_of_product = image,
                name_of_product = product_name,
                negotiable = negotiable,
                description = description,
                category = prod_category,
                active = True
                )
                ad_product = Product.objects.create(name=ad.name_of_product,
                price = ad.minimum_price,
                image = ad.sample_of_product,
                description = ad.description,
                category = ad.category
                )
                ad.product = ad_product
                ad.save()
            else:
                Ad.objects.create(
                    ad_category = ad_category,
                    seller = request.user.seller,
                    minimum_price = min_price,
                    maximum_price = max_price,
                    sample_of_product = image,
                    name_of_product = product_name,
                    negotiable = negotiable,
                    description = description,
                    category = prod_category,
                    active = False
                )
            return redirect(request.META.get('HTTP_REFERER'))
  
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
        ad_category = request.POST.cleaned_data.get('ad_category')
        product_name = request.POST.cleaned_data.get('product_name')
        negotiable = request.POST.cleaned_data.get('negotiable')
        fixed_price = request.POST.cleaned_data.get('fixed_price')
        min_price = request.POST.cleaned_data.get('minimum_price')
        max_price = request.POST.cleaned_data.get('maximum_price')
        image = request.POST.cleaned_data.get('product_image')
        print(ad_category)
        return redirect(request.META.get('HTTP_REFERER'))


def sponsoredAds(request):
    sup_ads = SponsoredAd.objects.all()
    paginator = Paginator(sup_ads, 25) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    parameter = request.GET.get("q")
    context = {
        'sup_ads':sup_ads,
        'page_obj':page_obj,
        'title':'Indus-Mega Farms'
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

    return render(request,'ads/sponsoredad.html',context)
    
