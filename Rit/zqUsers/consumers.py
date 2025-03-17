# your_app/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer

class ActivationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = 'activation_status'
        self.room_group_name = f'activation_{self.room_name}'

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'activation_status_update',
                'status': status
            }
        )

    async def activation_status_update(self, event):
        status = event['status']

        await self.send(text_data=json.dumps({
            'status': status
        }))
