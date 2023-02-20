from django.urls import path
from carecenter import views as user_views
from .views import (
    Appointment_Table_For_Receptionists_TodayArchiveView,
    Appointment_Table_For_carecenter_TodayArchiveView,
    TimeSlotCreateView,
    Booking_appointment_In_CareCenter_CreateView,

    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,

    CareCenter_Head_TodayArchiveView,
CareCenterSignUpView,
CareCenterCreateView,
Doctor_For_HeadDetailView,
Doctor_For_HeadUpdateView,
CareCenter_For_HeadUpdateView,
TimeSlotUpdateView,

)
from . import views
from users import views as user_views1
#from users.views import Table1ListView

urlpatterns = [
#Creating User Id  For CareCenter
    path('accounts/signup/reception/', user_views.CareCenterSignUpView.as_view(), name='reception_signup'),
#Creating Profile(detail) For CareCenter
    path('CareCenter_as_user_profile/', user_views.CareCenter_as_user_profile, name='CareCenter_as_user_profile'),


# CareCenter

    path('CareCenter/', Appointment_Table_For_Receptionists_TodayArchiveView.as_view(), name='CareCenter'),

    path('Appointment_Table_For_carecenter/<int:pk>/', Appointment_Table_For_carecenter_TodayArchiveView.as_view(),
         name='Appointment_Table_For_carecenter'),

    path('Appointment_Table_For_carecenter/<int:pk>/<int:str>/Booking_Appointment_form/', Booking_appointment_In_CareCenter_CreateView.as_view(),
         name='Booking_Appointment_form'),

# Creating User From Carecenter
    path('Appointment_Table_For_carecenter/<int:pk>/<int:str>/Booking_Appointment_form/user_register/', user_views.register_user, name='register'),



# Creating TimeSlots
    path('Appointment_Table_For_carecenter/<int:pk>/TimeSlotCreated_by_CareCenter/', TimeSlotCreateView.as_view(),
         name='timeslot_form'),

    path('TimeSlotUpdateView/<int:pk>/', TimeSlotUpdateView.as_view(),
         name='TimeSlot_update'),



# Center__Head   (This Links Are Shown or used only for Head

    path('CareCenter_Head/', CareCenter_Head_TodayArchiveView.as_view(),
         name='CareCenter_Head'),

    path('CareCenterCreateView_IN_HEAD/', CareCenterSignUpView.as_view(), name='CareCenterSignUp'),

    path('CareCenterCreateView_IN_HEAD/create', CareCenterCreateView.as_view(), name='CareCenterCreate'),

    path('DoctorDetail_For_HeadView/<int:pk>/', Doctor_For_HeadDetailView.as_view(),
         name='Doctor_For_HeadDetailView'),
    path('Doctor_For_HeadUpdateView/<int:pk>/', Doctor_For_HeadUpdateView.as_view(),
         name='Doctor_For_HeadUpdateView'),

    path('CareCenter_For_HeadUpdateView/<int:pk>/', CareCenter_For_HeadUpdateView.as_view(),
         name='CareCenter_For_HeadUpdateView'),

    path('create_Head/', user_views.Create, name='Create'),


#CareCenter_employee
    path('employee_list/', EmployeeListView.as_view(), name='Employee'),
    path('employee_detail/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/new/<int:pk>/', EmployeeCreateView.as_view(), name='employee_form'),
    path('employee/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]

