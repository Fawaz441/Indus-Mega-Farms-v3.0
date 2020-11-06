from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Challenger,Complaint,SpecialMessage,Message

CATEGORIES = (
    ('S','Join as a Student/Individual'),
    ('F','Join as a Farmer'),
    ('C','Join as a Company')
)

class ProfilePicForm(forms.Form):
    pic = forms.ImageField()
    

# Sign up form
class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    class Meta:
        fields = ("first_name","last_name","username","email","password1","password")
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["password2"].required=False
        self.fields["password2"].widget=forms.HiddenInput()
    def clean(self,*args,**kwargs):
        super().clean(*args,**kwargs)
        password = self.cleaned_data.get("password1")
        password_check = self.cleaned_data.get("password")
        if password != password_check:
            raise forms.ValidationError("Passwords do not match!")

        
# Student form
class StudentForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    location = forms.CharField(max_length=20)


CROP_VARIETIES = (
    ('Tubers','Tubers'),
    ('Grains','Grains'),
    ('Vegetables','Vegetables'),
    ('Fruits','Fruits'),
)
# Farmer form
class FarmerForm(forms.Form):
    farm_name = forms.CharField(label="Farm Name")
    location = forms.CharField()
    land_size = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1/2 acre'}))
    major_products = forms.ChoiceField(choices=CROP_VARIETIES,help_text='Choose the varieties you mostly deal with',required=False)
    other_products = forms.CharField(max_length=100,required=False,label='Fill if you do not deal with any of those crops')
    phone_number = forms.CharField(max_length=20)
    does_livestock = forms.BooleanField(label='Do you deal with livestock?',required=False)
    
# Company Form
class CompanyForm(forms.Form):
    company_name = forms.CharField()
    location = forms.CharField()
    phone_number = forms.CharField()


# Delivery form
class DeliveryForm(forms.Form):
    location = forms.CharField(widget=forms.TextInput(attrs={'id':'location_getter'}))



class ChallengerForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address',widget=forms.EmailInput(attrs={'placeholder':'Your email'}))
    class Meta:
        model = Challenger
        fields = '__all__'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = Challenger.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("User already signed up for IMchallenge updates.")
        return email


class ComplaintForm(forms.ModelForm):
    complaint = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Complaint
        fields = ["complaint"]

class CategoryForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES,widget=forms.RadioSelect)

# add to views
class SpecialMessageForm(forms.ModelForm):
    class Meta:
        model = SpecialMessage
        fields = ("title","user","message")


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["message"].label = "Special Message"

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("title","message")
