
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import homepage,about,ads_txt
# from ads.views import sponsoredAds

urlpatterns = [
      # path('competitions/',include('i_competitions.urls'))                                              #competitions
      path('oginni/', admin.site.urls),                                                               #admin
      path('',homepage,name='home'),     
      path('ads/',include('ads.urls')),                                                                 #homepage
      path('user/',include('users.urls')),                                                            #users
      path('products/',include('products.urls')),                                                     #products
      path('about/',about,name='about'),                                                              #about us
      url(r"^referrals/", include("pinax.referrals.urls", namespace="pinax_referrals")),              #pinax referrals
      url(r"^account/", include("account.urls")),                                                     #django-user-accounts(for pinax to work smoothly)
      path('paystack',include(('paystack.urls','paystack'),namespace='paystack')),                    #paystack
      path('blog/',include('blog.urls')), 
      path('summernote/', include('django_summernote.urls')),    
      path('management/',include('administration.urls')), 
      path('ads.txt',ads_txt,name='google_ads.txt')       
]

if settings.DEBUG:
      urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

