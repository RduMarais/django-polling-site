from django.db import models
import datetime
from django.utils import timezone

QUESTION_TYPES = (
        ('PL', 'Poll'),
        ('QZ', 'Quizz'),
        ('WC', 'Word Cloud'),
    )

class Question(models.Model):
    title = models.CharField('Question', max_length=50)
    desc = models.TextField('Description', max_length=200)
    pub_date = models.DateTimeField('Date Published')
    featured = models.BooleanField('Feature in Featured Polls Page')
    is_public = models.BooleanField('Is public in polls page',default=False)
    question_type = models.CharField('Type of Question', max_length=2,choices=QUESTION_TYPES, default='PL')

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

    def save(self, *args, **kwargs):
        choices = self.choice_set.all()
        is_quizz=False
        if(len(choices)==0):
            self.question_type = "WC"
        for choice in choices:
            if(choice.isTrue):
                is_quizz = True
        if(is_quizz):
            self.question_type = "QZ"
            print("yes")
        super(Question, self).save(*args, **kwargs)

    recent.admin_order_field = 'pub_date'
    recent.boolean = True


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    isTrue = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

