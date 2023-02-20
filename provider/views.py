from django.shortcuts import render,reverse, redirect, HttpResponse\
    , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import  CommentForm
from django.views.generic import (ListView,DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.list import MultipleObjectMixin
from users.models import  Timeslots
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView, TodayArchiveView
from django.shortcuts import get_object_or_404, render
from .forms import User, DoctorSignUpForm
import datetime
from users.models import  Appointment_Table
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import *
import calendar
from datetime import datetime, timedelta, date


#  Doctor_Login_point_______

def doctors_as_user_profile(request):
    return render(request, 'doctor/user_profile_for_doctors.html')

#creating User id and password for doctor
class DoctorSignUpView(CreateView):
    model = doctor
    form_class = DoctorSignUpForm
    template_name = 'doctor/doctor_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.CareCenter_Head_a = self.request.user.email
        user = form.save()
   #     user.set_password(user.password)
        login(self.request, user)
        return redirect('DoctorCreateView')

#creating Doctor's Profile
class DoctorCreateView(CreateView):
    model = doctor
    fields = [ 'CareCenter','First_Name','Last_Name', 'speciality','timing','experience','about','treatment','fee','home_address']
    template_name = 'doctor/create_doctors_profile_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


















#First_Page When Doctor Login's

class Table1ListView(ListView):
    model = Appointment_Table
    template_name = 'doctor/Front_Page_for_dr.html'
    context_object_name = 'all_appointment_for_dr'
    ordering = ['-date_posted']
    paginate_using = Appointment_Table
    paginate_by = 5
    make_object_list = True
    allow_future = True
    allow_empty = True
    def get_queryset(self):
        users = get_object_or_404(doctor,  user=self.request.user)
        return Appointment_Table.objects.filter(doctors_profile=users)

    def get_context_data(self, **kwargs):
        user = get_object_or_404(doctor, user=self.request.user)
        object_list = Appointment_Table.objects.filter(doctors_profile=user)
        context = super(Table1ListView, self).get_context_data(object_list=object_list, **kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        d = get_date(self.request.GET.get('date', None))
        context['prev_day'] = prev_day(d)
        context['next_day'] = next_day(d)
        context['today'] = next_day(d)
        context['appointments_booked'] = Appointment_Table.objects.filter(doctors_profile=user, appointment_date=d).extra(
            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')
        context['event'] = Timeslots.objects.filter(doctors_profile=user, available=True,
                                                    appointment_date=d).extra(
            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')
        p = Paginator(Appointment_Table.objects.select_related().filter(doctors_profile=user), self.paginate_by)
        context['table1s'] = p.page(context['page_obj'].number)
        return context



#Doctors Profile seen by Customers

class DoctorDetailView( FormMixin,DetailView, MultipleObjectMixin):
    model = doctor
    template_name = 'users/doctors_profile_archive.html'
    paginate_using = Appointment_Table
    paginate_by = 20
    context_object_name = "Table1s"
    form_class = CommentForm
    def get_context_data(self, **kwargs):
        object_list = Appointment_Table.objects.filter(doctors_profile=self.kwargs['pk'])
        context = super(DoctorDetailView, self).get_context_data(object_list=object_list, **kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        d = get_date(self.request.GET.get('date', None))
        context['prev_day'] = prev_day(d)
        context['next_day'] = next_day(d)
        context['today'] = next_day(d)

        context['event'] = Timeslots.objects.filter(doctors_profile=self.kwargs['pk'], available=True,
                                                    appointment_date=d).extra(
            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')

        context['appointments_booked'] = Appointment_Table.objects.filter(doctors_profile=self.kwargs['pk'], appointment_date=d).extra(
            select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')

        context['form'] = CommentForm(initial={'doctor': self.object})
        p = Paginator(Appointment_Table.objects.select_related().filter(doctors_profile=self.kwargs['pk']), self.paginate_by)
        context['table1s'] = p.page(context['page_obj'].number)
        return context

    def post(self, request, pk):
       post = get_object_or_404(doctor, pk = self.kwargs['pk'])
       form = CommentForm(request.POST)
       if form.is_valid():
           obj  = form.save(commit=False)
           obj.post = post
           obj.user = self.request.user
           obj.save()
           return redirect('doctors_profile_archive', post.pk)








# Arraging Appointments list according to Date wise

class Table1TodayArchiveView(TodayArchiveView):
    model = Appointment_Table
    allow_future = True
    date_field = 'appointment_date'
    make_object_list = True
    template_name = 'users/archive_day.html'
    allow_empty = True
    paginate_by = 4
    def get_queryset(self):
       return Appointment_Table.objects.filter(doctors_profile=self.request.user.email)
    def get_context_data(self, **kwargs):
        context = super(Table1TodayArchiveView, self).get_context_data( **kwargs)
        context['event'] = Timeslots.objects.filter(doctors_profile=self.kwargs['pk'], available=True).extra(select={'myinteger': 'CAST(no AS INTEGER)'}).order_by('myinteger')
        return context

class Table1ArchiveView(ArchiveIndexView, MultipleObjectMixin):
    model = Appointment_Table
    date_field = 'appointment_date'
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'users/archive_day.html'
    paginate_by = 2
    def get_queryset(self):
        dr_id = get_object_or_404(doctor, email=self.request.user.email)
        return Appointment_Table.objects.filter(doctors_profile=dr_id.id)
    def get_context_data(self, **kwargs):
        context = super(Table1ArchiveView, self).get_context_data( **kwargs)
        return context

class Table1YearArchiveView(YearArchiveView):
    model = Appointment_Table
    date_field = 'appointment_date'
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'users/archive_day.html'
    paginate_by = 2
    def get_queryset(self):
       return Appointment_Table.objects.filter(doctors_profile=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super(Table1YearArchiveView, self).get_context_data( **kwargs)
        context['event'] = Appointment_Table._meta.get_field('timeslot').choices
        return context

class Table1MonthArchiveView(MonthArchiveView):
    model = Appointment_Table
    allow_future = True
    date_field = 'appointment_date'
    make_object_list = True
    template_name = 'users/archive_day.html'
    allow_empty = True
    def get_queryset(self):
       return Appointment_Table.objects.filter(doctors_profile=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super(Table1MonthArchiveView, self).get_context_data( **kwargs)
        context['event'] = Appointment_Table._meta.get_field('appointment_date').choices
        return context

class Table1DayArchiveView(DayArchiveView):
    model = Appointment_Table
    date_field = 'appointment_date'
    month_format = '%m'
    make_object_list = True
    allow_future = True
    template_name = 'users/archive_day.html'
    allow_empty = True
    paginate_by = 4
    def get_queryset(self):
        return Appointment_Table.objects.filter(doctors_profile=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super(Table1DayArchiveView, self).get_context_data( **kwargs)
        context['event'] = Appointment_Table._meta.get_field('appointment_date').choices
        return context





#Comment Section in Doctors Profile_Commented by users

class CommentDetailView(DetailView):
    model = Comment
    template_name = "users/comment_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter()
        return context

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        Comment = self.get_object()
        if self.request.user == Comment.user:
            return True
        return False
    def get_success_url(self):
        return reverse('doctors_profile_archive', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(SuccessMessageMixin,LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    success_message = 'Your Comment has been updated'
    def form_valid(self, form):
        return super().form_valid(form)
    def test_func(self):
        Comment = self.get_object()
        if self.request.user == Comment.user:
            return True
        return False
    def get_success_url(self):
        return reverse('doctors_profile_archive', kwargs={'pk': self.kwargs['pk']})








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

