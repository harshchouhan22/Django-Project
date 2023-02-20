from django import forms
from .models import  CareCenter
from users.models import  CustomUser

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


#Create Center form for _receptions
class CareCenterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [ 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_CareCenter = True
        if commit:
            user.save()
        return user


class CareCenterUpdateForm(forms.ModelForm):
    class Meta:
        model = CareCenter
        fields = ['no_of_employees']
