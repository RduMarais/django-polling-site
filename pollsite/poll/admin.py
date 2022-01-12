from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Question, Choice, Meeting, Attendee

# administration of choices once in Question admin panel
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    readonly_fields = ['votes']

# Question admin panel
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_type','is_done']}),
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
    list_display = ('title', 'activities','participants','has_started')
    search_fields = ['title','description']

# Attendee score table
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'score','get_meeting') 
    fields = ['name','score']
    readonly_fields =['name', 'score','meeting']
    list_filter=('meeting',)

    class Meta:
        verbose_name = 'Score Table'

    def get_meeting(self,obj):
        link=reverse("admin:poll_meeting_change", args=[obj.meeting.id])
        return format_html('<a href="%s">%s</a>' % (link,obj.meeting.title))

admin.site.register(Question, QuestionAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Attendee, AttendeeAdmin)
