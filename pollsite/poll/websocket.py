"""
Websocket Handler for Pollsite

https://jaydenwindle.com/writing/django-websockets-zero-dependencies/
"""

from django.urls import resolve
from .connection import WebSocket

# this defines a parallel application for websockets
async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        match = resolve(scope["path"]) # followed comment on medium tuto
        match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)

