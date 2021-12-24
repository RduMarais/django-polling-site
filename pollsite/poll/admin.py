from django.contrib import admin

from .models import Question, Choice, Meeting


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'question_type','is_public', 'pub_date', 'participants') 
    # also 'recent is avzailable'
    list_filter = ['pub_date']
    search_fields = ['title']


class QuestionsOrder(admin.TabularInline):
    model = Question
    extra = 1

class MeetingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title','desc','meeting_date']}),
    ]
    inlines = [QuestionsOrder]
    list_display = ('title', 'activities','meeting_date')
    list_filter = ['meeting_date']
    # search_fields = ['title']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Meeting, MeetingAdmin)
