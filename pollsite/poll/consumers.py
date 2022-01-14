# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class QuestionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'] # this is the format that should be modified

        self.send(text_data=json.dumps({
            'message': message
        }))