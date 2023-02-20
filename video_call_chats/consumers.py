import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from django.contrib.auth.models import User
from blog.managers import Thread
from video_call_chats.models import ChatModel
from channels.db import database_sync_to_async



class ChatConsumer2(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name =  self.room_name

        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected!')

    # Receive message from WebSocket
    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        peer_username = receive_dict['peer']
        action = receive_dict['action']
        message = receive_dict['message']

        # print('unanswered_offers: ', self.unanswered_offers)

        print('Message received: ', message)

        print('peer_username: ', peer_username)
        print('action: ', action)
        print('self.channel_name: ', self.channel_name)
        print('self.room_group_name: ', self.room_group_name)

        if (action == 'new-offer') or (action == 'new-answer'):
            # in case its a new offer or answer
            # send it to the new peer or initial offerer respectively

            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            print('Sending to ', receiver_channel_name)

            # set new receiver as the current sender
            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict,
                }
            )

            return

        # set new receiver as the current sender
        # so that some messages can be sent
        # to this channel specifically
        receive_dict['message']['receiver_channel_name'] = self.channel_name

        # send to all peers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict,
            }
        )

    async def send_sdp(self, event):
        receive_dict = event['receive_dict']

        this_peer = receive_dict['peer']
        action = receive_dict['action']
        message = receive_dict['message']

        await self.send(text_data=json.dumps({
            'peer': this_peer,
            'action': action,
            'message': message,
        }))






# Doctor To Patient Personal Chat
class PersonalChat(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']


#        thread_obj = Thread.objects.get_or_create_personal_thread(loggedIn_user, other_user)
     #   self.room_group_name = f'presonal_thread_{thread_obj.id}'

        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async

    def save_message(self, username, thread_name, message):
        ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name)