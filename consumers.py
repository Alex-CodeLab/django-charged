from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from .api import Ln
from .decorators import postpone
from .models import Invoice

import uuid
import json

class LncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #try:
        #    self.chan_hash = self.scope['session']['_auth_user_hash']
        #except:
        self.chan_hash = str(uuid.uuid4())
        self.chan_hash = self.chan_name

        await self.channel_layer.group_add(
            self.chan_hash,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(self.chan_name, {
                'type': 'chan_message',
                'message': self.chan_name
            })


    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data = json.loads(text_data)
            if text_data['message_type'] == "wait_invoice":

                await self.channel_layer.send(
                    "lnws",
                    {
                        "type": "waitinvoice",
                        "group_id": self.chan_hash,
                        "payment_hash": text_data['payment_hash']
                    }
                )
        except:
            pass

    # Receive message from chan_hash group
    async def chan_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



    async def disconnect(self, close_code):
        # Leave group
        try:
            await self.channel_layer.group_discard(
                self.self.chan_hash,
                self.channel_name)
        except:
            pass

# use decorator only when using ./manage runserver
# @method_decorator(postpone, 'waitinvoice')
class WorkerConsumer(AsyncConsumer):

    async def waitinvoice(self, message):
        params = {}
        params['payment_hash'] = message['payment_hash']
        try:
            result = Ln().invoice_wait(params)
            if 'paid_at' in result.keys():
                Invoice.objects.filter(rhash=params['payment_hash']).update(status=result['status'], pay_index=result['pay_index'])

                await self.channel_layer.group_send(message['group_id'], {
                    'type': 'chan_message',
                    'message': "paid"
                })
        except:
            # error or timeout
            pass
