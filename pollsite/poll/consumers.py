# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Choice, Question, Meeting,Attendee,Vote

class QuestionConsumer(WebsocketConsumer):
	def connect(self):
		meeting_id = self.scope['url_route']['kwargs']['meeting_id']  
		self.meeting = Meeting.objects.get(pk=meeting_id)
		self.meeting_group_name = 'meeting_'+str(self.meeting.id)

		attendee_id = self.scope['session']['attendee_id']
		self.attendee = Attendee.objects.get(pk=attendee_id)
		# print("WS cnnect start : attendee = "+str(self.attendee.name))

		# Join group
		# don't think i need to setup a channel group here as there is no socket-to-socket
		#   communication or logic required
		async_to_sync(self.channel_layer.group_add)(
			self.meeting_group_name,
			self.channel_name
		)

		# print("WS cnnect OK")

		self.accept()

	# leave group
	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.meeting_group_name,
			self.channel_name
		)


	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message_in = text_data_json['message']  # this is the format that should be modified

		message_out = "test NOK"
		print('WS received get question')
		question = self.meeting.current_question()
		print('WS received get question OK')

		# si recoit message : question-test -> changer pour Next question
		if(message_in == "question-test"):
			print('WS received question test ok')
			message_out = {
				'message' : "test ok",
				'question':{
					'title': question.title,
					'desc': question.desc_rendered,
					'type': question.question_type,
				},
			}

		print(message_out)

		self.send(text_data=json.dumps(message_out))

	def send_question(self,question):
		# message_in = event['message']
		# Send question to channel
		self.send(text_data=json.dumps({
			'message': question.title
		}))

