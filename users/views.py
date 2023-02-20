from django.shortcuts import render,reverse, redirect, HttpResponse\
    , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import (ListView,DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.list import MultipleObjectMixin
from .models import doctor, Appointment_Table
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView, TodayArchiveView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .forms import User
import datetime
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .models import User,  CustomUser, Appointment_Table
from django.views.generic import TemplateView

from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView, View
from django.views.generic import TemplateView
from .forms import UserRegisterForm
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe

from users.models import CustomUser, Profile,Timeslots,Appointment_Table


from .utils import Calendar
from datetime import timedelta, date
import calendar

from datetime import datetime, timedelta


class SignUpView(TemplateView):
    context_object_name = "signupview"
    template_name = 'users/signup.html'



def appointments(request, pk=None):
    if pk:
        post_owner = get_object_or_404(User, pk=pk)
        user_posts = Appointment_Table.objects.filter(user=request.user)
    else:
        post_owner = request.user
        user_posts = Appointment_Table.objects.filter(patient_name_id=request.user)
    return render(request, 'users/appointments.html', {'post_owner': post_owner, 'user_posts': user_posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password'),

            template = get_template('users/user_id_pass_in_email.html')
            context = {
                'email': email,
                'password': password,
            }
            context = template.render(context)

            email = EmailMessage(
                "chouhanharsh256@gmail.com",
                context,
                "EVE health care center" + '',
                [email],
                headers={'Reply-To': email}
            )
   #         email.send()

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


#User's Profile
@login_required
def profile(request):
    if request.method == 'POST':
       u_form = UserUpdateForm(request.POST, instance=request.user)
       p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

       if u_form.is_valid() and p_form.is_valid():
             u_form = u_form.save(commit=True)
             u_form.save()
             p_form.save()

             messages.success(request, f'Your account has been updated!')
             return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)






#User's Profile Update
@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_update.html', context)


#Search on Front of Website For Users
def search(request):
    query = request.GET['query']
    if len(query) > 78:
        alldoctors = doctor.objects.none()
    else:
        alldoctorsname = doctor.objects.filter(First_Name__icontains=query)
        alldoctorstiming = doctor.objects.filter(timing__icontains=query)
        alldoctorsspeciality = doctor.objects.filter(speciality__icontains=query)
        alldoctorstreatment = doctor.objects.filter(treatment__icontains=query)
     #   alldoctorsaddress = doctor.objects.filter(CareCenter__icontains=query)
        alldoctors = alldoctorsname.union(alldoctorstiming, alldoctorsspeciality, alldoctorstreatment)
    if alldoctors.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'alldoctors': alldoctors, 'query': query}
    return render(request, 'users/search.html', params)



#Appointment list search

def appointmentsearch(request):
    query = request.GET['query']
    if len(query) > 78:
        allTable1s = Appointment_Table.objects.none()
    else:
        allTable1sAppointment_date = Appointment_Table.objects.filter(Appointment_date__icontains=query)
        allTable1sFirst_Name = Appointment_Table.objects.filter(First_Name__icontains=query)
        allTable1sLast_Name = Appointment_Table.objects.filter(Last_Name__icontains=query)
        allTable1stiming = Appointment_Table.objects.filter(timing__icontains=query)
        allTable1s = allTable1sAppointment_date.union(allTable1stiming, allTable1sFirst_Name, allTable1sLast_Name )
    if allTable1s.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allTable1s': allTable1s, 'query': query}
    return render(request, 'users/appointmentsearch.html', params)


class UserTable1ListView(ListView):
    model = Appointment_Table
    paginate_by = 5
    template_name = 'users/user_Table1s.html'
    context_object_name = 'table1s'
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Appointment_Table.objects.filter(patient_name=user).order_by('-date_posted')

from django.http import FileResponse, Http404
class Table1DetailView(DetailView):
    model = Appointment_Table
    fields = [ 'no', 'timing', 'your_name', 'doctors_profile', 'rimage','receipt']
    template_name = 'users/Table1_detail.html'

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from urllib import request
from django.template.loader import render_to_string


from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'kbzk1DSbJiV_03p5'
import urllib.request

class Table1CreateView(LoginRequiredMixin, CreateView):
    model = Appointment_Table
    fields = ['mode']

    def form_valid(self, form):
        form.instance.patient_name = self.request.user
        form.instance.doctors_profile_id = self.kwargs['pk']

        form.instance.CareCenter = doctor.objects.get(id=self.kwargs['pk']).CareCenter

        form.instance.Amount = doctor.objects.get(id=self.kwargs['pk']).fee

        form.instance.First_Name = self.request.user.First_Name
        form.instance.Last_Name =self.request.user.Last_Name

        obj = Timeslots.objects.filter(id=self.kwargs['str']).update(available=False)

        form.instance.start_time = Timeslots.objects.get(id=self.kwargs['str']).start_time
        form.instance.end_time = Timeslots.objects.get(id=self.kwargs['str']).end_time
        form.instance.appointment_date = Timeslots.objects.get(id=self.kwargs['str']).appointment_date
        form.instance.no = Timeslots.objects.get(id=self.kwargs['str']).no

        form.instance.timeslots_id = self.kwargs['str']
     #   start_date = Timeslots.objects.get(id=self.kwargs['str'])

        form.instance.timeslots_available = False
        mode=form.cleaned_data.get('mode'),
        your_name=form.cleaned_data.get('your_name'),
        timing=form.cleaned_data.get('timing'),
        no=form.cleaned_data.get('no'),
        for_date=form.cleaned_data.get('date'),
        regards=form.cleaned_data.get('regards'),
        payment=form.cleaned_data.get('payment'),

        template = get_template('users/doctors_app_email.html')
        context = {
            'no':no,
            'your_name' :your_name,
            'timing':timing,
            'for_date':for_date,
            'regards':regards,
            'payment':payment,
        }
        context = template.render(context)

        email = EmailMessage(
            "eveheathcarecenter@gmail.com",
            context,
            "EVE health care center" + '',
            doctor.objects.filter(id=self.kwargs['pk']),
            [self.request.user.email],
            headers={'Reply-To': self.request.user.email}
        )
#        email.send()
        return super().form_valid(form)

  #  def get(self, request, *args, **kwargs):
#        param_dict = {
 #           'MID': 'WorldP64425807474247',
  #          'ORDER_ID': str('1'),
   #         'TXN_AMOUNT': str('200'),
    #        'CUST_ID': 'chouhanharsh256@gmail.com',
     #       'INDUSTRY_TYPE_ID': 'Retail',
      #      'WEBSITE': 'WEBSTAGING',
       #     'CHANNEL_ID': 'WEB',
        #    'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

 #       }
  #      param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
       # return render(request, 'payment/paytm.html', {'param_dict': param_dict})

    def get_success_url(self):
            return reverse('doctors_profile_archive', kwargs={'pk': self.kwargs['pk'], })


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'payment/paymentstatus.html', {'response': response_dict})

from django.core.files import File
from io import BytesIO
from carecenter.models import CareCenter
from django.template.loader import get_template
from .utils import render_to_pdf
class Table1UpdateView(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment_Table
    fields = ['Writing_prescription', 'receipt']
#    success_message = 'Your Appointment has been updated'
    success_url = '/'
    template_name = 'users/Appointment_Table_update.html'

    def form_valid(self, form):
        Writing_prescription = form.cleaned_data.get('Writing_prescription')

        Patient_First_Name = Appointment_Table.objects.get(id=self.kwargs['pk']).First_Name
        Patient_Last_Name = Appointment_Table.objects.get(id=self.kwargs['pk']).Last_Name
        mode = Appointment_Table.objects.get(id=self.kwargs['pk']).mode
        Amount = Appointment_Table.objects.get(id=self.kwargs['pk']).Amount
        Appointment_date = Appointment_Table.objects.get(id=self.kwargs['pk']).appointment_date

        doctors_name = Appointment_Table.objects.get(id=self.kwargs['pk']).doctors_profile
        dr_First_Name = doctor.objects.get(email=doctors_name).First_Name
        dr_Last_Name = doctor.objects.get(email=doctors_name).Last_Name
        doctors_timing = doctor.objects.get(email=doctors_name).timing
        doctors_treatment = doctor.objects.get(email=doctors_name).treatment
        doctors_speciality = doctor.objects.get(email=doctors_name).speciality

        center_name = Appointment_Table.objects.get(id=self.kwargs['pk']).CareCenter.center_name
        Center_contact = Appointment_Table.objects.get(id=self.kwargs['pk']).CareCenter.center_contact
        Center_no = Appointment_Table.objects.get(id=self.kwargs['pk']).CareCenter.storeno
        receptionists_name = Appointment_Table.objects.get(id=self.kwargs['pk']).CareCenter.receptionists_name
        Address = Appointment_Table.objects.get(id=self.kwargs['pk']).CareCenter.Address

        template = get_template('users/prescription.html')

        context = {
            "Writing_prescription": Writing_prescription,
            "Patient_First_Name": Patient_First_Name,
            "Patient_Last_Name": Patient_Last_Name,
            "mode": mode,
            "Amount": Amount,
            "Appointment_date": Appointment_date,

            "dr_First_Name": dr_First_Name,
            "dr_Last_Name": dr_Last_Name,
            "doctors_timing": doctors_timing,
            "doctors_speciality": doctors_speciality,
            "doctors_treatment": doctors_treatment,

            "Center_contact": Center_contact,
            "CareCenter_name": center_name,
            "Center_no": Center_no,
            "Center_address": Address,
            "receptionists_name": receptionists_name,
        }
        html = template.render(context)
      #  return HttpResponse(html)
        pdf = render_to_pdf('users/prescription.html', context)
        if pdf:
            receipt_file = BytesIO(pdf.content)
            purch_upd = Appointment_Table.objects.get(id=self.kwargs['pk'])
            filename = 'purchase_%s.pdf' % (purch_upd)
            purch_upd.receipt = File(receipt_file, filename)
            purch_upd.save()
            form.instance.receipt = purch_upd.receipt
        #    return HttpResponse(pdf, content_type='application/pdf')

        return super().form_valid(form)

    def test_func(self):
        if self.request.user == Appointment_Table.doctors_profile :
            return True
        return True


class Table1DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment_Table
    success_url = '/'

    def test_func(self):
        table1 = self.get_object()
        if self.request.user == Appointment_Table.patient_name:
            return True
        return False














