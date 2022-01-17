from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Question, Choice, Meeting, Attendee, Vote

# administration of choices once in Question admin panel
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 1
	readonly_fields = ['votes']

# Question admin panel
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['question_type','is_done','meeting']}),
		('Question Information', {'fields': ['title', 'desc']}),
		('Date Information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInline]
	list_display = ('title', 'question_type','is_done', 'get_meeting', 'participants') 
	list_editable = ('is_done',)
	search_fields = ['title','description']

	def get_meeting(self,obj):
		link=reverse("admin:poll_meeting_change", args=[obj.meeting.id])
		return format_html('<a href="%s">%s</a>' % (link,obj.meeting.title))

# Question choices once in the meeting admin panel
#   this view extends the SortableStackedLine type to have the questions sortable
class QuestionsOrder(SortableStackedInline):
	model = Question
	extra = 0
	fields = (('is_done','question_type'))
	readonly_fields = ['question_type']
	show_change_link = True


# Meeting admin panel
class MeetingAdmin(NonSortableParentAdmin):
	fieldsets = [
		(None, {'fields': ['has_started','participants','date_start','date_end']}),
		('Meeting informations', {'fields': ['title','desc','image']}),
		('Parameters',{'fields':['code','reward_fastest']})
	]
	readonly_fields =['participants']
	inlines = [QuestionsOrder]
	list_display = ('title', 'activities','participants','is_ongoing')
	search_fields = ['title','description']

	def is_ongoing(self,obj):
		if(obj.date_start <= timezone.now() and obj.date_end >= timezone.now()):
			return 'Ongoing Meeting'
		elif(obj.date_end <= timezone.now()):
			return 'Past Meeting'
		elif(obj.date_start >= timezone.now()):
			return 'Future Meeting'
		else:
			return 'Schedule Error'

# Attendee score table
class LeaderBoard(admin.ModelAdmin):
	# name = 'Leader Board'
	# verbose_name = 'Score Table'
	list_display = ('name', 'score','get_meeting') 
	fields = ['name','score']
	readonly_fields =['name', 'score','meeting']
	list_filter=('meeting',)
	ordering = ('-score',)

	def __str__(self):
		 return "Leader Board"

	def get_meeting(self,obj):
		link=reverse("admin:poll_meeting_change", args=[obj.meeting.id])
		return format_html('<a href="%s">%s</a>' % (link,obj.meeting.title))

class VoteAdmin(admin.ModelAdmin):
	readonly_fields =['choice', 'user']
	list_display =('choice', 'get_user','id')

	def get_user(self,obj):
		return obj.user.name

admin.site.register(Question, QuestionAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Attendee, LeaderBoard)
if(settings.DEBUG):
	admin.site.register(Vote, VoteAdmin) # for debug
