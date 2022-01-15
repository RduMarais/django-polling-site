# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

from .models import Choice, Question, Meeting,Attendee,Vote
from .views import get_previous_user_answers

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


		# si recoit message : question-test -> changer pour Next question
		if(message_in == "question-start"):
			print('WS received question test ok')
			question = self.meeting.current_question()
			self.send_question(question)
		elif(message_in == "vote"):
			print('WS received vote')
			async_to_sync(self.receive_vote(text_data_json))
		else:
			message_out = "{'message':'error'}"
			print(message_out)
			self.send(text_data=message_out)

	# sync method
	def receive_vote(self,text_data_json):
		print('Vote : started receiving')
		try:
			question = self.meeting.current_question()
			choice = question.choice_set.get(pk=text_data_json['choice'])
			# I volontarily set the question based on user input to prevent async to sync
			# question = Question.objects.get(pk=text_data_json['question'])
			print('Vote : choice and question fetched')
			if(len(get_previous_user_answers(self.attendee,question))==0):
				print('Vote : fist vote')
				vote=Vote(user=self.attendee,choice=choice)
				vote.save()
				print('Vote : vote saved')

				if(choice.isTrue):
					if(question.first_correct_answer):
						question.first_correct_answer = False
						question.save()
						self.attendee.score +=1
					self.attendee.score +=1
					self.attendee.save()
				print('Vote : ok')
				message_out = {'message':'voted'}
			else:
				print('Vote : already voted')
				message_out = {'message':'error : already voted'}
		except:
			print('Vote : error happened')
			message_out = {'message':'error : something happened'}
		else:
			self.send(text_data=json.dumps(message_out)) #


	def send_question(self,question):
		
		message_out = {
			'message' : "question-go",
			'question':{
				'title': question.title,
				'desc': question.desc_rendered,
				'type': question.question_type,
				'id': question.id,
				'choices':[]
			},
		}
		for choice in question.choice_set.all():
			choice_obj = {
				'id':choice.id,
				'text':choice.choice_text,
			}
			message_out['question']['choices'].append(choice_obj)
		print(message_out)
		self.send(text_data=json.dumps(message_out))

