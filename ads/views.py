from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import AdCategory,Seller,Ad
from .forms import SellerForm


# View for all the ad_categories
def ad_categories_view(request):
    ad_categories = AdCategory.objects.all()
    context = {
        'title':'Ads',
        'ad_categories':ad_categories,
    }
    return render(request,'ads/index.html',context)


def ad_category_detail(request,name):
    form = SellerForm()
    seller_query = Seller.objects.filter(user=request.user)
    if seller_query.exists():
        has_seller = True
    else:
        has_seller = False
    if request.method == 'POST':
        if 'details_to_start' in request.POST:
            form = SellerForm(request.POST)
            seller_form = form.save(commit=False)
            seller_form.user = request.user
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
            if(negotiable == 'on'):
                negotiable = True
            else:
                negotiable = False
            if min_price == '':
                min_price = 0
            if max_price == '':
                max_price = 0
            Ad.objects.create(
                ad_category = ad_category,
                seller = request.user.seller,
                minimum_price = min_price,
                maximum_price = max_price,
                sample_of_product = image,
                name_of_product = product_name,
                negotiable = negotiable,
                description = description,
                category = prod_category
            )
            return redirect(request.META.get('HTTP_REFERER'))
    ad_category = get_object_or_404(AdCategory,name=name)
    context = {
        'title':ad_category.name,
        'ad_category':ad_category,
        'has_seller':has_seller,
        'form':form,
    }
    # if request.user in ad_category.users.all():
    try:
        user_ads = Ad.objects.filter(ad_category=ad_category,seller=request.user.seller)
        context['user_ads'] = user_ads
        if user_ads.exists():
            context['category_user_ads_count'] = user_ads.count
    except:
        context['category_user_ads_count'] = 0

    
    return render(request,'ads/detail.html',context)


def create_ad(request):
    if request.method == 'POST':
        ad_category = request.POST.cleaned_data.get('ad_category')
        product_name = request.POST.cleaned_data.get('product_name')
        negotiable = request.POST.cleaned_data.get('negotiable')
        fixed_price = request.POST.cleaned_data.get('fixed_price')
        min_price = request.POST.cleaned_data.get('minimum_price')
        max_price = request.POST.cleaned_data.get('maximum_price')
        image = request.POST.cleaned_data.get('.product_image')
        print(ad_category)
        return redirect(request.META.get('HTTP_REFERER'))