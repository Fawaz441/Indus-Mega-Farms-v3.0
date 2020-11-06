from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,View
from django.contrib.auth import get_user_model,login,authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,reverse,render,Http404
from django.dispatch import receiver


from pinax.referrals.models import Referral
from account.views import SignupView as BaseSignupView
from .models import Student,Farmer,Company,ReferralCode,Message,SpecialMessage,ProfilePictures,CompanySellerPlan,FarmerPlan,IMNews
from .forms import StudentForm,FarmerForm,CompanyForm,SignUpForm,AdvertForm,ComplaintForm,CategoryForm,ProfilePicForm
from products.models import Order
from indus_mega_farms.utils import newsletter
from paystack.views import payment_verified

User = get_user_model()


# Dashboard
@login_required()
def user_home(request):
    title = "Dashboard"
    newsletter(request)
    pending_orders = Order.objects.filter(ordered=True,delivered=False,user=request.user).all()
    if pending_orders.exists():
        pending_orders = pending_orders
    messages_ = Message.objects.all().order_by('-created_date')
    news = IMNews.objects.all()
    special_messages = SpecialMessage.objects.filter(user=request.user).order_by('-created_date')
    rank = ReferralCode.objects.all()
    ranks = list(rank)
    user_rank = ReferralCode.objects.filter(user__username=request.user.username)
    position=""
    if user_rank.exists():
        rank = ranks.index(user_rank.first())
        if str(rank)[-1] == "2":position = "nd"
        elif str(rank)[-1]=="1":position="st"
        elif str(rank)[-1]=="3":position="rd"
        else:position="th"
    else:
        rank = ""
    if request.method=='POST':
        pic_form = ProfilePicForm(request.POST,request.FILES)
        if pic_form.is_valid():
            pic = pic_form.cleaned_data.get('pic')
            user_pic,created = ProfilePictures.objects.get_or_create(user=request.user)
            user_pic.profile_pic = pic
            user_pic.save()
            return redirect('users:user_home')
    else:
        pic_form = ProfilePicForm()
    
    context = {"title":title,"pending_orders":pending_orders,'rank':rank,'position':position,'general_messages':messages_,'special_messages':special_messages,'pic_form':pic_form
    ,'news':news}
    farm_qs = Farmer.objects.filter(user=request.user)
    company_qs = Company.objects.filter(user=request.user)
    if farm_qs.exists():
        farmer = farm_qs.first()
        farmer_plan = FarmerPlan.objects.filter(subscribee=farmer)
        if farmer_plan.exists():
            farmer_plan = farmer_plan.first()
            context['has_plan'] = True
            context['customers'] = farmer_plan.customers
            context['plan_type'] = farmer_plan.category
    if company_qs.exists():
        company = company_qs.first()
        company_plan = CompanySellerPlan.objects.filter(subscribee=company)
        if company_plan.exists():
            company_plan = company_plan.first()
            context['has_plan'] = True
            context['customers'] = company_plan.patronages
    return render(request,"users/user_home.html",context=context)


# Signing up
class SignupView(BaseSignupView):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def generate_username(self, form):
        pass

    def after_signup(self, form):
        super(SignupView, self).after_signup(form)
        action = Referral.record_response(self.request, "USER_SIGNUP")
        if action is not None:
            referral = Referral.objects.get(id=action.referral.id)
            code_inter = ReferralCode.objects.get(code=referral)
            code_inter.referred+=1
            code_inter.save()
        # May need to login user here
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")


        user = authenticate(username=username,password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        SpecialMessage.objects.create(
            user=user,
            title = 'Welcome',
            message = "Welcome to Indus Mega Farms, {}".format(user.username)
        )
        login(self.request,user)
    
        referral = Referral.objects.create(
        user=self.request.user,
        redirect_to=reverse("users:signup")
        )
        referral_code = ReferralCode.objects.create(
            code = referral,
            user = self.request.user
        )
        referral_code.save()

    def create_profile(self, form):
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        category = form.cleaned_data.get("category")
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")

       
# Selecting category
def choice(request):
    title = "Select Category"
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            if category == "C":
                return redirect("users:company_reg")
            elif category == "F":
                return redirect("users:farmer_reg")
            elif category == "S":
                return redirect("users:student_reg")
        if form.errors:
            messages.info(request,form.errors)
    else:
        form = CategoryForm()
    return render(request,'users/choices.html',{'form':form,"title":title})




# Student details reg
class StudentReg(View):
    def get(self,*args, **kwargs):
        title = "Register as a Student"
        form = StudentForm()
        return render(self.request,'users/student_form.html',{'form':form,"title":title})
    
    def post(self,*args, **kwargs):
        form = StudentForm(self.request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            location = form.cleaned_data.get('location')
            student = Student.objects.create(
                phone_number = phone_number,
                location=location,
                user = self.request.user,
            )
            student.save()
            messages.success(self.request,'Successfully registered')
            return redirect('users:user_home')
            
        else:
            messages.warning(self.request,'Form not valid')
            return redirect('users:student_reg')
        
# Farmer's detail reg
class FarmerReg(View):
    def get(self,*args, **kwargs):
        form = FarmerForm()
        title = "Register as a Farmer"
        return render(self.request,'users/farmer_form.html',{'form':form,"title":title})
    
    def post(self,*args, **kwargs):
        form = FarmerForm(self.request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            location = form.cleaned_data.get('location')
            farm_name = form.cleaned_data.get('farm_name')
            land_size = form.cleaned_data.get('land_size')
            major_products = form.cleaned_data.get('major_products')
            other_products = form.cleaned_data.get('other_products')
            does_livestock = form.cleaned_data.get('does_livestock')
            farmer = Farmer.objects.create(
                user = self.request.user,
                land_size = land_size,
                location = location,
                farm_name = farm_name,
                major_products = major_products,
                other_products = other_products,
                does_livestock = does_livestock,
                phone_number = phone_number,
            )
            farmer.save()
            messages.success(self.request,'Successfully registered')            
        else:
            messages.warning(self.request,'Form not valid')
        return redirect('users:user_home')



# Company's detail reg
class CompanyReg(View):
    def get(self,*args, **kwargs):
        form = CompanyForm()
        title="Register as a Company"
        return render(self.request,'users/company_form.html',{'form':form,"title":title})
    
    def post(self,*args, **kwargs):
        form = CompanyForm(self.request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            location = form.cleaned_data.get('location')
            company_name = form.cleaned_data.get('company_name')
           
            company = Company.objects.create(
                user = self.request.user,
                phone_number = phone_number,
                location = location,
                company_name = company_name
            )
            company.save()
            messages.success(self.request,'Successfully registered')            
        else:
            messages.warning(self.request,'Form not valid')
        return redirect('users:user_home')




# Complaint form reg
@login_required
def complaint_form(request):
    title = 'Make a Complaint'
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.user=request.user
            advert.save()
            messages.info(request,"Your complaint will be reviewed shortly.Thank you")
            return redirect("users:user_home")
        else:
            messages.info(request,"Your form is not valid")
    else:
        form = ComplaintForm()
    context = {"title":title,"form":form}
    return render(request,"users/send_complaint.html",context)



   

# set harvest time
@login_required 
def set_harvest_time(request):
    farmer = Farmer.objects.get(user=request.user)
    if not farmer:
        return Http404
    farmer.harvest_time = True
    farmer.save()
    messages.info(request,"You are ready for harvest!")
    return redirect("users:user_home")

# Unset harvest time
@login_required 
def falsify_harvest_time(request):
    farmer = Farmer.objects.get(user=request.user)
    if not farmer:
        return Http404
    farmer.harvest_time = False
    farmer.save()
    messages.info(request,"Harvest Time not Ready")
    return redirect("users:user_home")



       