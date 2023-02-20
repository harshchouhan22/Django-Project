from django.contrib import admin
from .models import CareCenter, Carecenter_employee, CareCenter_Finance, CareCenter_Head
# Register your models here.
admin.site.register(CareCenter)
admin.site.register(Carecenter_employee)
admin.site.register(CareCenter_Finance)
admin.site.register(CareCenter_Head)