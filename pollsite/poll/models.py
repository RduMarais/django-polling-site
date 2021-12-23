from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    title = models.CharField('Question', max_length=50)
    desc = models.TextField('Description', max_length=200)
    pub_date = models.DateTimeField('Date Published')
    featured = models.BooleanField('Feature in Featured Polls Page')
    is_public = models.BooleanField('Is public in polls page',default=False)

    class Meta:
        abstract=True

    def __str__(self):
        return self.title

    def recent(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def participants(self):  
        participants = 0
        choices = self.choice_set.all()
        for choice in choices:
            participants += choice.votes
        return participants
        

    recent.admin_order_field = 'pub_date'
    recent.boolean = True


class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


##### POLL MODEL #####
class Poll(Question):
    question_type = "Poll"

class PollChoice(Choice):
    question = models.ForeignKey(Poll,on_delete=models.CASCADE)

##### QUIZZ MODEL #####
class Quizz(Question):
    question_type = "Quizz"

class QuizzChoice(Choice):
    question = models.ForeignKey(Quizz,on_delete=models.CASCADE)

##### WORDCLOUD MODEL #####
class WordCloud(Question):
    question_type = "WordCloud"

class WordCloudChoice(Choice):
    question = models.ForeignKey(WordCloud,on_delete=models.CASCADE)