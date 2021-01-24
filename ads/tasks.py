from django.utils import timezone
from celery import shared_task
from ads.models import Ad
from users.models import SpecialMessage

@shared_task(name='delete_expired_ads')
def terminate_expired_ads():
    expired_ads = Ad.objects.filter(ending_date__lte=timezone.now()).select_related('seller')
    for ad in expired_ads:
        seller = ad.seller.user
        message = f'Your ad {ad.name_of_product} has expired'
        title = 'Ad Expiry Notice'
        SpecialMessage.objects.create(user=seller,title=title,message=message)
        ad.delete()
    return None
        
        
        
