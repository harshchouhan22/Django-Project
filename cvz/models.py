from django.db import models
from django.utils import timezone
from doctor.models import *
from PIL import Image
from django.conf import settings

#ID For Head Of CareCenter
class CareCenter_Head(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(('email address'), unique=True)
    First_Name = models.CharField(max_length=128, blank=True)
    Last_Name = models.CharField(max_length=128, blank=True)
    birth_date = models.DateField( blank=True, null=True)
    phone_number = models.IntegerField()
    Address = models.CharField(max_length=300,blank=True)
    Carecenter_document = models.FileField(upload_to='carecenter_head', null=True, blank=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return  self.user.email



#CareCenters Profile , For Receptionists
class CareCenter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    CareCenter_Head = models.ForeignKey(CareCenter_Head, on_delete=models.CASCADE)
    email = models.EmailField(('email address'), unique=True)
    center_name = models.CharField(max_length=128)
    storeno = models.CharField(max_length=300)
    Address = models.CharField(max_length=300)
    no_of_doctors = models.CharField(max_length=100)
    no_of_employees = models.CharField(max_length=100)

    Carecenter_document = models.FileField(upload_to='carecenter_documents', null=True, blank=True)
    Carecenter_image = models.ImageField(upload_to='carecenter_image', null=True, blank=True)
    receptionists_name = models.CharField(help_text='', max_length=100)

    date_registered = models.DateTimeField(default=timezone.now)
    center_contact = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return  self.user.email



class Carecenter_employee(models.Model):
    CareCenter = models.ForeignKey(CareCenter, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=128, blank=True)
    Last_Name = models.CharField(max_length=128, blank=True)
    employee_image = models.ImageField( upload_to='employee_pics', blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    phone_number = models.IntegerField()
    Address = models.CharField(max_length=300,blank=True)
    Job_role = models.CharField(max_length=128, blank=True)
    About = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128)
    date_registered = models.DateTimeField(default=timezone.now)
    employee_document_1 = models.FileField(upload_to='carecenter_employees', null=True, blank=True)
    employee_document_2 = models.FileField(upload_to='carecenter_employees', null=True, blank=True)

    def __str__(self):
        return 'Emplyee of CareCenter'

    def save(self, *args, **kwargs):
        super(Carecenter_employee, self).save(*args, **kwargs)

        img = Image.open(self.employee_image.path)
#        img.thumbnail(output_size)
        img.save(self.employee_image.path)


class CareCenter_Finance(models.Model):
    CareCenter = models.ForeignKey(CareCenter, on_delete=models.CASCADE)
    Employee_salaries = models.CharField(max_length=120)
    Electricity_Bills = models.CharField(max_length=120)
    Revenue = models.CharField(max_length=100)
    Additional_Bills = models.FileField(upload_to='carecenter_finance', null=True, blank=True)


    def __str__(self):
        return 'Finance of CareCenter'


