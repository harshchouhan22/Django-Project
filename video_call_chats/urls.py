from django.urls import path

from video_call_chats import views


urlpatterns = [

#    path('chat_room/', views.chat_room, name='chat_room'),
    path('chatPage/<str:id>/', views.chatPage, name='chatPage'),

    path('video_youtube1/', views.peer1, name='peer1'),
    path('video_youtube2/', views.peer2, name='peer2'),

    path('video_call/<str:id>/', views.video_call, name='video_call'),

]
