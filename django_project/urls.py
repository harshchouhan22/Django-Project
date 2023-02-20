"""django_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

from users.views import (
    Table1DetailView,
    Table1CreateView,
    Table1UpdateView,
    Table1DeleteView,
    UserTable1ListView,

)

admin.site.site_header = "DRE Admin"
admin.site.site_title = "DRE Admin Panel"
admin.site.index_title = "Welcome to DRE Admin Panel"


#from django.conf.urls import  url



urlpatterns = [
    path('admin/', admin.site.urls),



    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', user_views.SignUpView.as_view(), name='signup'),





    path('register/', user_views.register, name='register'),


    path('search/', user_views.search, name='search'),

    path('shop/handlerequest/', user_views.handlerequest, name='handlerequest'),
    #
    #


#



    # For Create btn inside today page



    path('Table1/<int:pk>/', Table1DetailView.as_view(), name='Table1_detail'),









# For Users in doctors profile
    path('doctors_profile/<int:pk>/<int:str>/Table1_form/', Table1CreateView.as_view(), name='Appointment_Table_form'),

    path('Table1/<int:pk>/update/', Table1UpdateView.as_view(), name='Appointment_Table_update'),
    path('Table1/<int:pk>/delete/', Table1DeleteView.as_view(), name='Table1_confirm_delete'),
    path('user/<str:username>//', UserTable1ListView.as_view(), name='user_Table1s'),


    path('appointmentsearch/', user_views.appointmentsearch, name='appointmentsearch'),
    path('appointments/', user_views.appointments, name='appointments'),

    # Comment

    path('profile_update/', user_views.profile_update, name='profile_update'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/home.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),


    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),


    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    path('', include('blog.urls')),
    path('', include('video_call_chats.urls')),
    path('', include('doctor.urls')),
    path('', include('carecenter.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
