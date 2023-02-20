from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from doctor.models import *

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.db import models
#class User(AbstractUser):
 #   is_profile = models.BooleanField(default=False)
  #  is_doctor = models.BooleanField(default=False)
   # is_CareCenter = models.BooleanField(default=False)


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


#This For All Type OF User's
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=128, blank=True)
    Last_Name = models.CharField(max_length=128, blank=True)
    phone_number = models.IntegerField( blank=True, null=True)
    email = models.CharField(_('email address'),max_length=128, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_doctor = models.BooleanField(default=False)
    is_CareCenter = models.BooleanField(default=False)
    CareCenter_Head = models.BooleanField(default=False)


    Company_staff_1 = models.BooleanField(default=False)
    Company_staff_2 = models.BooleanField(default=False)
    Company_staff_3 = models.BooleanField(default=False)

#Attachement purpose
    is_doctor_a = models.CharField(max_length=128, blank=True, null=True)
    is_CareCenter_a = models.CharField(max_length=128, blank=True, null=True)
    CareCenter_Head_a = models.CharField(max_length=128, blank=True, null=True)


    Company_staff_1_a = models.CharField(max_length=128, blank=True, null=True)
    Company_staff_2_a = models.CharField(max_length=128, blank=True, null=True)
    Company_staff_3_a = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
     # return self.id

#User's Profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE )
    First_Name = models.CharField(max_length=128, blank=True)
    Last_Name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    phone_number = models.IntegerField(default='+91', blank=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 50:
            output_size = (100, 50)
            img.thumbnail(output_size)
            img.save(self.image.path)




from carecenter.models import CareCenter

from doctor.models import doctor
#Appointment_Timeslots
class Timeslots(models.Model):
    title = models.CharField(default='Available',max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    appointment_date = models.DateField(default=timezone.now)
    no = models.CharField(max_length=1000)
    available = models.BooleanField(default=True)
    doctors_profile = models.ForeignKey(doctor, on_delete=models.CASCADE)


    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return '%s - %s' % (self.start_time.strftime("%I:%M %p"), self.end_time.strftime("%I:%M %p"))

class Appointment_Table(models.Model):
    patient_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_name')
    doctors_profile = models.ForeignKey(doctor, on_delete=models.CASCADE)
    CareCenter = models.ForeignKey(CareCenter, on_delete=models.CASCADE)
    timeslots = models.OneToOneField(Timeslots, on_delete=models.CASCADE )
    First_Name = models.CharField(max_length=128)
    Last_Name = models.CharField(max_length=128)
    receipt = models.FileField(upload_to='prescription_receipts', null=True, blank=True)
    Writing_prescription = models.TextField(max_length=10000, null=True, blank=True)
    no = models.CharField(max_length=1000)
    mode = models.CharField(max_length=200, choices=(
          ('In Clinic', 'In Clinic'),('online(Video Calling)','online(Video Calling)'),) ,default='cash on center')
    Amount = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    appointment_date = models.DateField()

    def __str__(self):
        return self.id





