from django.contrib import messages
from users.models import NewLetter
from users.models import NewLetter
def newsletter(request):
    email = request.POST.get("news_email")
    
    if email:
        email_qs = NewLetter.objects.filter(email=email)
        if email_qs.exists():
            messages.info(request,"This email is already subscribed to our newsletter")
        else:
            newsletter_sub = NewLetter.objects.create(
                email = email,
            )
            newsletter_sub.save()
            messages.info(request,"You have successfully suscribed to our newsletter")
        
