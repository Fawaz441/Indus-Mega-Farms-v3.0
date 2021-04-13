from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from .utils import newsletter
from users.forms import ChallengerForm


# Homepage View
@never_cache
def homepage(request):
    challenge_form = ChallengerForm(request.POST or None)
    if challenge_form.is_valid():
        messages.info(request,"Thank you!. You will get updates when due")
    context = {"challenge_form":challenge_form,"title":"Indus-Mega Farms"}
    newsletter(request)
    return render(request,"homepage.html",context)

# About Us View
def about(request):
    title = "About Indus-Mega"
    newsletter(request)
    return render(request,"about.html",{"title":title})


# ads.txt
def ads_txt(request):
    line = "google.com, pub-1372794899198889, DIRECT, f08c47fec0942fa0"
    return HttpResponse(line)
