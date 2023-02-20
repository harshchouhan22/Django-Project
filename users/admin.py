from django.contrib import admin
from .models import Profile, Appointment_Table, Timeslots

admin.site.register(Timeslots)
admin.site.register(Profile)
admin.site.register(Appointment_Table)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Company_Staff.models import Company_staff_2,Company_staff_1, Company_staff_3
from users.models import CustomUser


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email','First_Name','Last_Name', 'password', 'username', 'last_login')}),
        ('Permissions', {'fields': (
            'is_doctor',
            'is_CareCenter',
            'CareCenter_Head',
            'Company_staff_1',
            'Company_staff_2',
            'Company_staff_3',
            'is_doctor_a',
            'is_CareCenter_a',
            'CareCenter_Head_a',
            'Company_staff_1_a',
            'Company_staff_2_a',
            'Company_staff_3_a',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'username', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(CustomUser, UserAdmin)

