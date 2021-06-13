import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chat.models import Message, Room
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.label  = self.scope["url_route"]["kwargs"]["label"]
        self.room_group_name = f'chat_{self.label}'
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )
        await self.accept()
        print('connect')

    async def disconnet(self,close_code):
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
        )
        print('disconnect')

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_label = text_data_json["room_label"]
        username = text_data_json["sender"]
        await self.save_message(username,room_label,message)
        await self.channel_layer.group_send(
        self.room_group_name,{
        "type":"chat_message",
        "text":message,
        "sender":username
        })


    async def chat_message(self,event):
        message = event["text"]
        sender = event["sender"]
        print(event)
        await self.send(text_data=json.dumps({
        'text':message,
        "sender":sender
        }))


    @database_sync_to_async
    def save_message(self,sender,room_label,message):
        user = User.objects.get(username=sender)
        room = Room.objects.get(label=room_label)
        room.messages.create(sender=user,text=message)
        # message = Message(sender=sender,reciever=reciever,message=message)
        # message.save()
