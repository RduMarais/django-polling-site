from django.contrib import admin
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.utils.html import format_html
from django.urls import reverse
from django.forms import Select, CheckboxInput
from django.db import models

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Question, Choice, Meeting

# administration of choices once in Question admin panel
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

# Question admin panel
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_type','is_done']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'question_type','is_done', 'get_meeting', 'participants') 
    # also 'recent' and 'pub_date' are available
    list_editable = ('is_done',)
    list_filter = ['pub_date']
    search_fields = ['title']

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
        (None, {'fields': ['title','desc','has_started']}),
    ]
    inlines = [QuestionsOrder]
    list_display = ('title', 'activities','has_started')
    list_filter = ['has_started']
    # search_fields = ['title']



admin.site.register(Question, QuestionAdmin)
admin.site.register(Meeting, MeetingAdmin)
