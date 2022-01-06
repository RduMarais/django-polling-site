from django.contrib import admin
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.utils.html import format_html
from django.urls import reverse

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Question, Choice, Meeting

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public','question_type']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'question_type','is_public', 'get_meeting', 'participants') 
    # also 'recent' and 'pub_date' are available
    list_editable = ('is_public',)
    list_filter = ['pub_date']
    search_fields = ['title']

    def get_meeting(self,obj):
        link=reverse("admin:poll_meeting_change", args=[obj.meeting.id])
        return format_html('<a href="%s">%s</a>' % (link,obj.meeting.title))


class QuestionsOrder(SortableStackedInline):
    model = Question
    extra = 1

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
