from django.conf import settings
from django.db import models
from users.models import *
from carecenter.models import *

# Create your models here.
# for Doctor's Profile
class doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    CareCenter = models.ForeignKey(CareCenter, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    First_Name = models.CharField(max_length=128, blank=True)
    Last_Name = models.CharField(max_length=128, blank=True)
    speciality = models.CharField(max_length=300)
    timing = models.TextField(max_length=200)
    ceritificates_of_dr = models.FileField(upload_to='receipts', null=True, blank=True)
    experience = models.CharField(max_length=10)
    about = models.TextField(max_length=1000)
    treatment = models.TextField(max_length=1000)
    fee = models.CharField(max_length=200)
    email = models.EmailField(('email address'), unique=True)
    home_address = models.CharField(max_length=200)
    onn_off = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'name']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return  str(self.user.email)

from django.contrib.auth.models import User
from django.utils.timezone import now

class Comment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    doctor=models.ForeignKey(doctor, on_delete=models.CASCADE, related_name='comments')
   # parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)
    #approved_comment = models.BooleanField(default=True)



    class Meta:
        ordering = ['timestamp']

    def approve(self):
        self.approved_comment = True
        self.save()


    def __str__(self):
        return  "On Dr." + self.doctor.name[0:14] + " By" + " " + self.user.username

