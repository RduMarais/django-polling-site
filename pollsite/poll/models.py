from django.db import models
import datetime
from django.utils import timezone

from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

QUESTION_TYPES = (
        ('PL', 'Poll'),
        ('QZ', 'Quizz'),
        ('WC', 'Word Cloud'),
    )

class Meeting(models.Model):
    title = models.CharField('Title of Meeting', max_length=50)
    desc = models.TextField('Description', max_length=200)
    code = models.CharField('Security Code for joining the Meeting', default='P1F02021', max_length=50)
    has_started = models.BooleanField('Meeting has started',default=False)

    def activities(self):
        return len(self.question_set.all())

class Attendee(models.Model):
    name = models.CharField('Your Name', max_length=50, default='Anonymous')
    

class Question(SortableMixin):
    title = models.CharField('Question', max_length=50)
    desc = models.TextField('Description', max_length=200)
    pub_date = models.DateTimeField('Date Published')
    is_done = models.BooleanField('Question already completed',default=False)
    question_type = models.CharField('Type of Question', max_length=2,choices=QUESTION_TYPES, default='PL')
    meeting = SortableForeignKey(Meeting, on_delete=models.CASCADE)
    question_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/models/options/#order-with-respect-to
        # order_with_respect_to = 'meeting'
        ordering = ['question_order'] 

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

