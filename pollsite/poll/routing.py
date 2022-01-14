# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # path('ws/<int:question_id>', consumers.QuestionConsumer.as_asgi()),
    re_path(r'ws/(?P<question_id>\w+)/$', consumers.QuestionConsumer.as_asgi()),
]