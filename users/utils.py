# # Subscription to plans

# # Farmer's view of 3 plans
# class FarmerSubscribeView(View,LoginRequiredMixin):
#     def get(self,request,*args,**kwargs):
#         farmer_qs = Farmer.objects.get(user=self.request.user)
#         if not farmer_qs:
#             return Http404
#         else:
#             return render(request,'users/farmers_subscribe.html')

# # Farmer gold plan
# class FarmGoldPlanDetailView(View,LoginRequiredMixin):
#     def get(self, request, *args, **kwargs):
#         farmer = Farmer.objects.filter(user=request.user).first()
#         if not farmer:
#             return Http404
#         farmer_plan_qs = FarmerPlan.objects.filter(subscribee=farmer)
#         if farmer_plan_qs.exists():
#             subscribed_plan = farmer_plan_qs.first()
#             messages.info(request,"You're already subscribed to the Farmer {} plan".format(subscribed_plan.category))
#             return redirect('users:user_home')
#         self.request.session['gold'] = True
#         context = {'amount':500,'email':self.request.user.email}
#         return render(request,'users/gold.html',context)
  
# # Farmer silver plan
# class FarmSilverPlanDetailView(View,LoginRequiredMixin):
#     def get(self, request, *args, **kwargs):
#         farmer = Farmer.objects.filter(user=request.user).first()
#         if not farmer:
#             return Http404
#         farmer_plan_qs = FarmerPlan.objects.filter(subscribee=farmer)
#         if farmer_plan_qs.exists():
#             subscribed_plan = farmer_plan_qs.first()
#             messages.info(request,"You're already subscribed to the Farmer {} plan".format(subscribed_plan.category))
#             return redirect('users:user_home')
#         self.request.session['silver'] = True
#         print(self.request.session['silver'])
#         context = {'amount':250,'email':self.request.user.email}
#         return render(request,'users/silver.html',context)
   

# # Farmer premium plan
# class FarmPremiumPlanDetailView(TemplateView,LoginRequiredMixin):
#     def get(self, request, *args, **kwargs):
#         farmer = Farmer.objects.filter(user=request.user).first()
#         if not farmer:
#             return Http404
#         farmer_plan_qs = FarmerPlan.objects.filter(subscribee=farmer)
#         if farmer_plan_qs.exists():
#             subscribed_plan = farmer_plan_qs.first()
#             messages.info(request,"You're already subscribed to the Farmer {} plan".format(subscribed_plan.category))
#             return redirect('users:user_home')
#         self.request.session['premium'] = True
#         context = {'amount':100,'email':self.request.user.email}
#         return render(request,'users/premium.html',context)
    


# #company seller plan
# class CompanySellerPlanView(View,LoginRequiredMixin):
#     def get(self,request,*args,**kwargs):
#         redirect_field_name = 'users:login'
#         context = {'amount':300,'email':self.request.user.email}
#         self.request.session['company_sole'] = True
#         return render(request,'users/company_seller.html',context=context)