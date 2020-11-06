from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import LockdownEntryForm
from .models import ExactLockdownEntries

@login_required
def smart_naija_lockdown(request):
    if request.method == 'POST':
        form = LockdownEntryForm(request.POST,request.FILES)
        entry_qs = ExactLockdownEntries.objects.filter(user=request.user)
        if form.is_valid():
            if entry_qs.exists():
                messages.info(request,"You have already submitted an entry!")
                return redirect("users:user_home")
            else:
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                messages.info(request,'Your entry has been successfully submitted')
                return redirect('home')
    else:
        form = LockdownEntryForm()
    return render(request,'competitions/smart_lockdown.html',context={'form':form,'title':'Smart Farmers Naija Lockdown'})
