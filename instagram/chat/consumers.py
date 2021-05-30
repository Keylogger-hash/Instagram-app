import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from asgiref.sync import async_to_sync
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

    async def disconnet(self,close_code):
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
        )

    async def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        await self.channel_layer.group_send(
        self.room_group_name,{
        "type":'chat_message',
        "message":message
        })


    async def chat_message(self,event):
        message = event["message"]
        print(message)
        await self.send(text_data=json.dumps({
        'message':message
        }))

    @async_to_sync
    def save_message(self,sender,reciever,message):
        message = Message(sender=sender,reciever=reciever,message=message)
        message.save()
