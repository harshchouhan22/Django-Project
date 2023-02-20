from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile, doctor, Appointment_Table
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import  User, doctor
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


from django.contrib.auth import login
from django.shortcuts import render,reverse, redirect, HttpResponse, get_object_or_404

class UserRegisterForm(UserCreationForm):
    First_Name = forms.CharField( label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    Last_Name = forms.CharField( label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone_number = forms.IntegerField( widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    email = forms.CharField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email/Phone'}))
    class Meta:
        model = User
        fields = [ 'First_Name', 'Last_Name','phone_number', 'email', 'password1' ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_profile = True
        user.save()
        return user
    def form_valid(self, form):
        user = form.save()

        login(self.request, user)
        return redirect('/')




class UserUpdateForm(forms.ModelForm):
   # username = models.CharField(max_length='128')
    class Meta:
        model = User
        fields = [ 'phone_number', 'First_Name','Last_Name']



class ProfileUpdateForm(forms.ModelForm):


    birth_date = forms.DateField()

    class Meta:
        model = Profile
        fields = ['birth_date', 'image']










from django.forms import ModelForm, DateInput
from .models import Timeslots

