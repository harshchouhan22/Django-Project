from django.urls import path
from doctor import views as user_views
from .views import (
     CommentUpdateView,
DoctorDetailView,
Table1ListView,
CommentDetailView,
CommentDeleteView,
DoctorSignUpView,
DoctorCreateView,
)
from . import views
#from users.views import Table1ListView

urlpatterns = [

    path('doctors_profile/<int:pk>/', DoctorDetailView.as_view(),
         name='doctors_profile_archive'),


#    path('doctors_profile/<int:pk>/comment_form/', CommentCreateView.as_view(), name='comment_form'),

    path('doctors_profile/<int:pk>/comment_update/', CommentUpdateView.as_view(), name='comment_form'),

    path('doctors_profile/<int:pk>/comment_detail/', CommentDetailView.as_view(), name='comment_detail'),

    path('doctors_profile/<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment_confirm_delete'),





# Creating Credintials For Doctor Throught CareCenter___Head

#Creating Doctor's user id and password
    path('DoctorSignUpView/', DoctorSignUpView.as_view(),
         name='DoctorSignUpView'),

#Creating Doctors's Profile
    path('DoctorCreateView/profile_creating', DoctorCreateView.as_view(),
         name='DoctorCreateView'),





# This view is For Doctor As It Login's through user id and password

    path('doctors_as_user_profile/', user_views.doctors_as_user_profile, name='doctors_as_user_profile'),

    path('all_appointment_for_dr/', Table1ListView.as_view(), name='all_appointments_for_dr'),

    path('doctors_as_user_profile/', user_views.doctors_as_user_profile, name='doctors_as_user_profile'),







# Archieve Views
    path('archive_day/', user_views.Table1TodayArchiveView.as_view(),
         name='archive_day'),

    path('archive_day/Archieve/', user_views.Table1ArchiveView.as_view(),
         name='archive_day'),

    path('archive_day/<int:year>/', user_views.Table1YearArchiveView.as_view(),
         name='archive_day'),

    # Example: /blog/archive/2019/nov/
    path('archive_day/<int:month>/<int:year>/',
         user_views.Table1MonthArchiveView.as_view(month_format='%m'),
         name='archive_day'),

    # Example: /blog/archive/2019/nov/10/
    path("archive_day/<int:day>/<int:month>/<int:year>/",
         user_views.Table1DayArchiveView.as_view(),
         name='archive_day'),
]

