from django.contrib import admin
from .models import Student,Farmer,Company,Complaint,ReferralCode,Challenger,NewLetter,SpecialMessage,Message,ProfilePictures,CompanySellerPlan,FarmerPlan,IMNews

class AdvertAdmin(admin.ModelAdmin):
    list_display = ["name_of_product","location","minimum_price","maximum_price","created_date"]
    list_filter = ["name_of_product","created_date","location"]

class ComplaintAdmin(admin.ModelAdmin):
    list_filter = ["created_date"]
    list_display = ["attended_to","created_date"]

class MessageAdmin(admin.ModelAdmin):
    list_display =["title","message"]
    
class SpecialMessageAdmin(admin.ModelAdmin):
    list_display =["title","user","message"]

class FarmerPlanAdmin(admin.ModelAdmin):
    list_display = ['subscribee','category', 'customers', 'acheived']

class CompanySellerAdmin(admin.ModelAdmin):
    list_display = ['subscribee', 'patronages' ,'acheived']
admin.site.register(IMNews)
admin.site.register(CompanySellerPlan,CompanySellerAdmin)
admin.site.register(FarmerPlan,FarmerPlanAdmin)
admin.site.register(ProfilePictures)
admin.site.site_header = "Indus-Mega Farms"
admin.site.register(NewLetter)
admin.site.register(SpecialMessage,SpecialMessageAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Challenger)
admin.site.register(ReferralCode)
admin.site.register(Complaint,ComplaintAdmin)
admin.site.register(Student)
admin.site.register(Farmer)
admin.site.register(Company)
