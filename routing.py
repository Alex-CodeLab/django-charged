from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter
from .consumers import LncConsumer, WorkerConsumer
from django.conf.urls import url
from channels.sessions import SessionMiddlewareStack



application = ProtocolTypeRouter({
    "websocket":SessionMiddlewareStack(
        URLRouter([
            url("^lightning/ws$", LncConsumer),
        ])),
    'channel': ChannelNameRouter({
        'lnws': WorkerConsumer,
    }),
})
