from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question, Meeting,Attendee
from .forms import WordForm,LoginForm

# Index view with all current meetings
def index(request):
	meetings_list = Meeting.objects.filter(has_started=True)
	context = {'meetings':meetings_list }
	return render(request, 'poll/index', context)

# Once you enter a meeting, this is the page displaying the currnt question and previous results
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
			'current_question': meeting.question_set.filter(is_done=False).order_by('question_order')[0],
			'previous_question_list': meeting.question_set.filter(is_done=True).order_by('question_order') 
		}
		return render(request, 'poll/meeting', context) 

def login(request,meeting_id):
	meeting = get_object_or_404(Meeting, pk=meeting_id)
	if(not 'attendee_id' in request.session): # if attendee is not logged in yet
		if(request.method=='POST'):
			form = LoginForm(request.POST)
			if(form.is_valid()):
				new_attendee = Attendee(name=form.cleaned_data['username'],meeting=meeting,score=0)
				new_attendee.save()
				request.session['attendee_id'] = new_attendee.id
				return HttpResponseRedirect(reverse('poll:meeting', args=(meeting.id,)))
			else:
				return render(request,'poll/login',{'meeting':meeting})
		else:
			return render(request,'poll/login',{'meeting':meeting})
	else:
		return HttpResponseRedirect(reverse('poll:meeting', args=(meeting.id,)))



# return view for word clouds -> returns to add template
def added(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	form = WordForm()
	return render(request, 'poll/add', {'question': question,'form':form})

# form view for word clouds
def add(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.method == 'POST':
		form = WordForm(request.POST)
		if(form.is_valid()):
			try:
				existing_choice = question.choice_set.get(choice_text=form.cleaned_data['choice'])
				existing_choice.votes +=1
				existing_choice.save()
			except (KeyError, Choice.DoesNotExist):
				added_choice = Choice(question=question, choice_text=form.cleaned_data['choice'], votes=1)
				added_choice.save()
			return HttpResponseRedirect(reverse('poll:added', args=(question_id,)))
	else:
		form = WordForm()
	return render(request, 'poll/add', {'question': question,'form':form})

# return view for Polls and Quizz
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'poll/results', {'question': question})


# form view for Text, Polls and Quizz
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'poll/vote', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
