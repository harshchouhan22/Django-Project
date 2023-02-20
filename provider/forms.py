from django import forms
from users.models import  Appointment_Table
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Comment, doctor
User = get_user_model()
from users.models import  CustomUser

class DoctorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [ 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user

class Appointment_TableUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment_Table
        fields = ['Writing_prescription']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=2000)
    class Meta:
        model = Comment
        fields = ['comment', 'doctor']
