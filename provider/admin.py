from django.contrib import admin
from .models import doctor, Comment
# Register your models here.

admin.site.register(Comment)

admin.site.register(doctor)