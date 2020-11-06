from django.urls import path
from .views import smart_naija_lockdown

app_name = 'competitions'

urlpatterns = [
    path('smart_farmers_naija_lockdown',smart_naija_lockdown,name='lockdown_comp')
]