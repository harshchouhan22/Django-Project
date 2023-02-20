from users.forms import UserUpdateForm
from .forms import CareCenterUpdateForm, CareCenterSignUpForm
from users.models import Appointment_Table, Timeslots
from doctor.models import doctor
from .models import *
from users.forms import UserRegisterForm
from django.shortcuts import render,reverse, redirect
from django.views.generic import (ListView,DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.dates import TodayArchiveView
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
import datetime
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.shortcuts import render
import calendar
from datetime import datetime, timedelta, date
from users.models import CustomUser, Profile
from django.forms import ModelForm, DateInput


# This Entire Section IS For CareCenter__Head __User



#Create CareCenter_ Login At Reception_Login _Credintials
class CareCenterSignUpView(CreateView):
    model = CareCenter
    form_class = CareCenterSignUpForm
    template_name = 'Head/create_carecenter_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Receptionists'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        form.instance.CareCenter_Head_a = self.request.user.email
        user = form.save()
        login(self.request, user)
        return redirect('CareCenterCreate')

#Adding Data To CareCenter Details
class CareCenterCreateView(LoginRequiredMixin,CreateView):
    model = CareCenter
    fields = [ 'CareCenter_Head','center_name', 'storeno','Address','no_of_doctors','no_of_employees','receptionists_name','center_contact']
    template_name = 'Head/create_carecenter_profile_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user
        return super().form_valid(form)

#Carecenter_Head_Front Page
class CareCenter_Head_TodayArchiveView(TodayArchiveView):
    model = Appointment_Table
    allow_future = True
    date_field = 'appointment_date'
    make_object_list = True
    template_name = 'Head/First_page.html'
    allow_empty = True
    paginate_using = Appointment_Table
    paginate_by = 2
    context_object_name = 'CareCenter_Head'

    def get_context_data(self, **kwargs):
        context = super(CareCenter_Head_TodayArchiveView, self).get_context_data( **kwargs)
        context['CareCenter_Head'] = CareCenter_Head.objects.filter(user=self.request.user)
        context['CareCenter'] = CareCenter.objects.filter(CareCenter_Head=self.request.user.CareCenter_Head)
        user = get_object_or_404(CareCenter, CareCenter_Head=self.request.user.CareCenter_Head)
        context['doctor'] = doctor.objects.filter(CareCenter=user)
        return context

class Doctor_For_HeadDetailView(DetailView):
    model = doctor
    template_name = 'Head/doctors_detail.html'

class Doctor_For_HeadUpdateView(UpdateView):
    model = doctor
    template_name = 'Head/doctor_update.html'
    fields = [ 'about', 'timing', 'First_Name', 'Last_Name']
    
    def get_success_url(self):
            return reverse('Doctor_For_HeadDetailView', kwargs={'pk': self.kwargs['pk'], })


class CareCenter_For_HeadUpdateView(UpdateView):
    model = CareCenter
    template_name = 'Head/Carecenter_update.html'
    fields = ['no_of_employees', 'no_of_doctors','receptionists_name','center_contact']
    success_url = '/'



def Create(request):
    return render(request, 'Head/create.html')

# End For CareCenter's ___Head





# Creating This Section For CareCenter___At Reception



#Front Page When Login At Reception
class Appointment_Table_For_Receptionists_TodayArchiveView(TodayArchiveView):
    model = Appointment_Table
    allow_future = True
    date_field = 'appointment_date'
    make_object_list = True
    template_name = 'blog/home.html'
    context_object_name = 'CareCenter'
    allow_empty = True
    paginate_using = Appointment_Table
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(Appointment_Table_For_Receptionists_TodayArchiveView, self).get_context_data( **kwargs)
        user = get_object_or_404(CareCenter, email=self.request.user)
        context['doctor'] = doctor.objects.filter(CareCenter=user)

        return context


# Profile Page For Carecenter_Id At Reception
@login_required
def CareCenter_as_user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        r_form = CareCenterUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.carecenter)
        if u_form.is_valid():
            u_form = u_form.save(commit=True)
            u_form.save()
            r_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        r_form = CareCenterUpdateForm(instance=request.user.carecenter)
    context = {
        'u_form': u_form,
        'r_form': r_form
    }
    return render(request, 'carecenter/CareCenter_as_user_profile.html', context)


#Doctors profile At Reception_In which Appointment _Table _is Displayed
class Appointment_Table_For_carecenter_TodayArchiveView(TodayArchiveView):
    model = Appointment_Table
    allow_future = True
    date_field = 'appointment_date'
    make_object_list = True
    template_name = 'carecenter/Appointment_Table_For_carecenter.html'
    allow_empty = True
    paginate_using = Appointment_Table
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(Appointment_Table_For_carecenter_TodayArchiveView, self).get_context_data( **kwargs)
        context['doctor'] = doctor.objects.all().filter(id=self.kwargs['pk'])

        d = get_date(self.request.GET.get('day', None))

        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        d = get_date(self.request.GET.get('date', None))
        context['prev_day'] = prev_day(d)
        context['next_day'] = next_day(d)
        context['today'] = next_day(d)
        context['appointments_booked'] = Appointment_Table.objects.all().filter(doctors_profile=self.kwargs['pk'],
                                                appointment_date=d).extra(
                            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')
        context['timeslot'] = Timeslots.objects.all().filter(available=True,doctors_profile=self.kwargs['pk'],
                                                appointment_date=d).extra(
                            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')
        return context


#Creating Booking_Appointments Through Receptionists
class Booking_appointment_In_CareCenter_CreateView(LoginRequiredMixin, CreateView):
    model = Appointment_Table
    fields = [ 'mode', 'patient_name']
    template_name = 'carecenter/Booking_Appointment_form.html'

    def form_valid(self, form):
        patient_name=form.cleaned_data.get('patient_name')
        cu = CustomUser.objects.get(email=patient_name).id

        usr_detail = Profile.objects.get(user=cu)

        form.instance.First_Name = CustomUser.objects.get(email=patient_name).First_Name
        form.instance.Last_Name = CustomUser.objects.get(email=patient_name).Last_Name

        form.instance.doctors_profile = Timeslots.objects.get(id=self.kwargs['str']).doctors_profile
        doctors_profile = Timeslots.objects.get(id=self.kwargs['str']).doctors_profile
        form.instance.CareCenter = doctor.objects.get(email=doctors_profile).CareCenter

        form.instance.timeslots_id = self.kwargs['str']

        obj = Timeslots.objects.filter(id=self.kwargs['str']).update(available=False)
        form.instance.start_time = Timeslots.objects.get(id=self.kwargs['str']).start_time
        form.instance.end_time = Timeslots.objects.get(id=self.kwargs['str']).end_time
        form.instance.appointment_date = Timeslots.objects.get(id=self.kwargs['str']).appointment_date
        form.instance.no = Timeslots.objects.get(id=self.kwargs['str']).no
        return super().form_valid(form)

    def get_success_url(self):
            return reverse('Appointment_Table_For_carecenter', kwargs={'pk': self.kwargs['pk'], })


#Creating User At Reception At the time of Appointment Booking
def register_user(request, pk, str):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password'),
         #   template = get_template('users/user_id_pass_in_email.html')
            context = {
                'email': email,
                'password': password,
            }
          #  context = template.render(context)
            email = EmailMessage(
                "chouhanharsh256@gmail.com",
                context,
                "EVE health care center" + '',
                [email],
                headers={'Reply-To': email}
            )
   #         email.send()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return reverse('Booking_Appointment_form', kwargs={'str': str })
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)



#Creating TimeSlots_Through _Receptionists
class TimeSlotCreateView(LoginRequiredMixin, CreateView):
    model = Timeslots
    fields = ['start_time', 'end_time', 'appointment_date', 'no','available']
    template_name = 'carecenter/timeslot_form.html'
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }

    def form_valid(self, form):
        cu = doctor.objects.get(id=self.kwargs['pk'])
        form.instance.doctors_profile = cu
        return super().form_valid(form)

    def get_success_url(self):
            return reverse('Appointment_Table_For_carecenter', kwargs={'pk': self.kwargs['pk'], })



class TimeSlotUpdateView(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Timeslots
    fields = ['start_time', 'end_time', 'appointment_date', 'no','available']
    template_name = 'carecenter/TimeSlots_update.html'

    def test_func(self):
        if self.request.user == Appointment_Table.patient_name :
            return True
        return True

    def get_success_url(self):
            return reverse('Appointment_Table_For_carecenter', kwargs={'pk': self.kwargs['pk'], })







#Employees of Carecenter

def Employee(request):
    context = {
        'employee_list': Carecenter_employee.objects.all()
    }
    return render(request, 'carecenter/employee_list.html', context)

class EmployeeListView(ListView):
    model = Carecenter_employee
    template_name = 'carecenter/employee_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'employee_list'

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Carecenter_employee
    fields = ['First_Name', 'Last_Name', 'birth_date','phone_number','email']
    template_name = 'carecenter/employee_form.html'

    def form_valid(self, form):
        form.instance.CareCenter = CareCenter.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
            return reverse('/')

class EmployeeDetailView(DetailView):
    model = Carecenter_employee
    fields = [ 'First_Name', 'Last_Name', 'birth_date','phone_number','email']
    template_name = 'carecenter/employee_detail.html'

class EmployeeUpdateView(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Carecenter_employee
    fields = ['First_Name', 'Last_Name', 'birth_date','phone_number','email']
    template_name = 'carecenter/employee_update.html'

class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Carecenter_employee
    success_url = '/'








#These Are Callendar's Dates Which i had Used IN Appointments_Table
def get_date(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def next_day(d):
    # Get today's date
    presentday = datetime.now()  # or presentday = datetime.today()
    # Get Yesterday
    prev_day = presentday
    nextday = 'date=' + str(prev_day.year) + '-' + str(prev_day.month) + '-' + str(prev_day.day)
    return nextday

def prev_day(d):
    # Get today's date
    presentday = datetime.now()  # or presentday = datetime.today()
    # Get Yesterday
    prev_day = presentday - timedelta(1)
    yesterday = 'date=' + str(prev_day.year) + '-' + str(prev_day.month) + '-' + str(prev_day.day)
    return yesterday
