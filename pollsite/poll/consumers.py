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

	# Receive message from meeting group
	def meeting_message(self, event):
		message = event['message']

		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'message': message
		}))


	# receive message from client
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
		elif(message_in == "debug-results"):
			print('WS received get-results')
			question = self.meeting.current_question()
			self.send_results(question)
		else:
			message_out = "{'message':'error'}"
			print(message_out)
			self.send(text_data=message_out)


	###### Functional logic #####

	# sync method
	def receive_vote(self,text_data_json):
		try:
			question = self.meeting.current_question()
			choice = question.choice_set.get(pk=text_data_json['choice'])
			# I volontarily set the question based on user input to prevent async to sync
			# question = Question.objects.get(pk=text_data_json['question'])
			print('Vote : choice and question fetched')
			if(len(get_previous_user_answers(self.attendee,question))==0):
				vote=Vote(user=self.attendee,choice=choice)
				vote.save()

				if(choice.isTrue and question.question_type =='QZ'):
					if(question.first_correct_answer):
						question.first_correct_answer = False
						question.save()
						self.attendee.score +=1
					self.attendee.score +=1
					self.attendee.save()

				
				if(question.question_type =='QZ'):
					message_out = {'message':'voted'}
					self.send(text_data=json.dumps(message_out)) #
				elif(question.question_type =='PL'):
					print('WS async notif update poll start')
					self.send_results(question)
					# OK
					# async update all users
					self.notify_update_PL(question,choice)
			else:
				message_out = {'message':'error : already voted'}
				self.send(text_data=json.dumps(message_out)) #
		except:
			message_out = {'message':'error : something happened'}
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

	def send_results(self,question):
		message_out = {
			'message' : "results",
			'results': [],
			'question_type':question.question_type,
			'total':question.participants(), #shamelessly reuse this function
		}
		for choice in question.choice_set.all():
			choice_obj = {
				'id':choice.id,
				'text':choice.choice_text,
				'votes':choice.votes(),
				'isTrue':choice.isTrue,
			}
			message_out['results'].append(choice_obj)
		print(message_out)
		self.send(text_data=json.dumps(message_out))

	def notify_update_PL(self,question,choice):
		print("WS start notify update Poll")
		async_to_sync(self.channel_layer.group_send)(
			self.meeting_group_name,
			{
				'type': 'meeting_message',
				'message': 'notify-update-poll',
				'vote': choice.id,
			}
		)
		print("group : update +choice.id")


