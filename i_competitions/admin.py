from django.contrib import admin
from .models import ExactLockdownEntries

class LockdownAdmin(admin.ModelAdmin):
    list_display = ['title','phone_number','slides','created_date']

admin.site.register(ExactLockdownEntries,LockdownAdmin)