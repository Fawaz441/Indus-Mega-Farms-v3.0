from django.urls import path,re_path
from django.shortcuts import redirect
from . import views
from django.contrib.auth.views import (LogoutView,LoginView,PasswordResetView,PasswordResetConfirmView,
PasswordResetDoneView,PasswordResetCompleteView,PasswordChangeView)

app_name = 'users'
urlpatterns = [
    path('category/',views.choice,name='category'),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user_home/', views.user_home, name='user_home'),
    path('reg/student',views.StudentReg.as_view(),name='student_reg'),
    path('reg/farmer',views.FarmerReg.as_view(),name='farmer_reg'),
    path('reg/company',views.CompanyReg.as_view(),name='company_reg'),
    path('reset_password',PasswordResetView.as_view(subject_template_name='users/subject_template.txt',email_template_name='users/email_template.html',template_name='users/password_reset.html',success_url = 'password_reset_done'),name='password_reset'),
    path('password_reset_done',PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    re_path('password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('change_password',PasswordChangeView.as_view(template_name='users/password_change.html',success_url='login'),name='password_change'),
    path('send_complaint',views.complaint_form,name='send_complaint'),
    # path('farmers_subscribe',views.FarmerSubscribeView.as_view(),name='farmers_subscribe'),
    # path('gold-farmer',views.FarmGoldPlanDetailView.as_view(),name='gold_farmer'),
    # path('silver-farmer',views.FarmSilverPlanDetailView.as_view(),name='silver_farmer'),
    # path('premium-farmer',views.FarmPremiumPlanDetailView.as_view(),name='premium_farmer'),
    # path('company_subscribe',views.CompanySellerPlanView.as_view(),name='company_subscribe'),
    path('harvest-time-ready',views.set_harvest_time,name='set_harvest_time'),
    path('harvest-time-not-ready',views.falsify_harvest_time,name='falsify_harvest_time'),
    ]