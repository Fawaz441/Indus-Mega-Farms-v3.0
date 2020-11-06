from .models import Seller
from django import forms

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['brand_name','phone_number','whatsapp_number','location']

