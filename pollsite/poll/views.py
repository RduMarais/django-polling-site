from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone

import datetime

from .models import Choice, Question, Meeting,Attendee,Vote
from .forms import WordForm,LoginForm

def get_previous_user_answers(attendee,question):
	query = Q(user=attendee)
	query.add(Q(choice__question__title__contains=question.title),Q.AND)
	return Vote.objects.filter(query)


# Index view with all current meetings
def index(request):
	# Gets all meetings happening now (defined with Start time and End Time)
	meetings_list = Meeting.objects.filter(Q(date_start__lte=timezone.now()) & Q(date_end__gte=timezone.now()))
	context = {'meetings':meetings_list }
	return render(request, 'poll/index', context)

# Once you enter a meeting, this is the page displaying the current question and previous results
def meeting(request, meeting_id):
	meeting = get_object_or_404(Meeting, pk=meeting_id)
	if(not 'attendee_id' in request.session): # if attendee is not logged in yet
		form = LoginForm()
		return render(request,'poll/login',{'meeting':meeting,'form':form})
	else:
		attendee = Attendee.objects.get(pk=request.session['attendee_id'])
		context = {
			'meeting':meeting,
			'attendee':attendee,
			'current_question': meeting.current_question(),
			'previous_question_list': meeting.question_set.filter(is_done=True).order_by('question_order') 
		}
		return render(request, 'poll/meeting', context)

def login(request,meeting_id):
	meeting = get_object_or_404(Meeting, pk=meeting_id)
	if(not 'attendee_id' in request.session): # if attendee is not logged in yet
		if(request.method=='POST'):
			form = LoginForm(request.POST)
			if(form.is_valid()):
				if(form.cleaned_data['meeting_code'] == meeting.code):
					new_attendee = Attendee(name=form.cleaned_data['username'],meeting=meeting,score=0)
					new_attendee.save()
					request.session['attendee_id'] = new_attendee.id
					return HttpResponseRedirect(reverse('poll:meeting', args=(meeting.id,)))
				else:
					context = {'meeting':meeting,'error':"The meeting code is not valid",'form':LoginForm()}
					return render(request,'poll/login',context)
			else:
				context = {'meeting':meeting,'error':"Something went wrong",'form':LoginForm()}
				return render(request,'poll/login',context)
		else:
			return render(request,'poll/login',{'meeting':meeting})
	else:
		return HttpResponseRedirect(reverse('poll:meeting', args=(meeting.id,)))



# return view for word clouds 
def cloud(request, question_id):
	if(not 'attendee_id' in request.session):
		form = LoginForm()
		return render(request,'poll/login',{'meeting':meeting,'form':form})
	else:
		question = get_object_or_404(Question, pk=question_id)
		form = WordForm()
		return render(request, 'poll/cloud', {'question': question,'form':form})


# return view for Polls and Quizz
def results(request, question_id):
	if(not 'attendee_id' in request.session):
		form = LoginForm()
		return render(request,'poll/login',{'meeting':meeting,'form':form})
	else:
		question = get_object_or_404(Question, pk=question_id)
		attendee = Attendee.objects.get(pk=request.session['attendee_id'])
		return render(request, 'poll/results', {'question': question})


