from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .utils import get_turn_info

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import ChatModel
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required


# Create your views here.
def chatPage(request,id):
    user_obj = CustomUser.objects.get(id=id)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'chatPage.html' ,context = {'id':id, 'user': user_obj, 'users': users, 'messages': message_objs})


@login_required
def video_call(request, id=id):
    user_obj = CustomUser.objects.get(id=id)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'video_call.html',context = {'id':id, 'user': user_obj, 'users': users, 'messages': message_objs})



# Create your views here.

def peer1(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'peer1.html', context=context)

def peer2(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'peer2.html', context=context)

def peer(request):
    # get numb turn info
    context = get_turn_info()
    print('context: ', context)

    return render(request, 'peer.html', context=context)



#def chat_room(request):
 #   users = User.objects.exclude(email=request.user.email)
  #  return render(request, 'chat_room.html', context={'users': users})

