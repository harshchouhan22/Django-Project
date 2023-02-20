from django.db import models
from users.models import CustomUser
# Create your models here.


#Company Staff_1
class Company_staff_1(models.Model):
    Company_staff_1 = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return  self.email

#company_Staff_2
class Company_staff_2(models.Model):
    Company_staff_2 = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return  self.email

#Company_Staff_3
class Company_staff_3(models.Model):
    Company_staff_2 = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return  self.email
