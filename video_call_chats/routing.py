from django.urls import re_path

from . import consumers

websocket_urlpatterns = [

    re_path(r'video_call/(?P<id>[^/]+)/$', consumers.ChatConsumer2.as_asgi()),

    re_path(r'chatPage/(?P<id>[^/]+)/$', consumers.PersonalChat.as_asgi()),


]
