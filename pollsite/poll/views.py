from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question, Meeting
from .forms import WordForm


def index(request):
    latest_question_list = Question.objects.filter(is_public=True).order_by('-pub_date')
    meetings_list = Meeting.objects.filter(has_started=True)
    context = {
        'latest_question_list': latest_question_list,
        'meetings':meetings_list,
    }
    return render(request, 'poll/index', context)

def meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    return render(request, 'poll/meeting', {'meeting': meeting})

def added(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = WordForm()
    return render(request, 'poll/add', {'question': question,'form':form})

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
                print("DOES NOT EXIST")
                added_choice = Choice(question=question, choice_text=form.cleaned_data['choice'], votes=1)
                added_choice.save()
            return HttpResponseRedirect(reverse('poll:added', args=(question_id,)))
    else:
        form = WordForm()
    return render(request, 'poll/add', {'question': question,'form':form})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results', {'question': question})


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
