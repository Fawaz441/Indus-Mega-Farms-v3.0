from .models import Seller
from django import forms

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['brand_name','phone_number','whatsapp_number','location']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['phone_number'].widget = forms.TextInput(attrs={'placeholder':'+234...'})
        self.fields['whatsapp_number'].widget = forms.TextInput(attrs={'placeholder':'+234...'})



