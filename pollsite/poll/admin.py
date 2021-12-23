from django.contrib import admin

from .models import Question, Choice, Poll,PollChoice,Quizz, QuizzChoice, WordCloud,WordCloudChoice

###### BASE MODELS #####
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'is_public', 'recent', 'pub_date', 'participants')
    list_filter = ['pub_date']
    search_fields = ['title']


###### POLLS #####

class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [PollChoiceInline]
    list_display = ('title', 'is_public', 'recent', 'pub_date', 'participants')
    list_filter = ['pub_date']
    search_fields = ['title']

###### QUIZZ #####

class QuizzChoiceInline(admin.TabularInline):
    model = QuizzChoice
    extra = 2

class QuizzAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [QuizzChoiceInline]
    list_display = ('title', 'is_public', 'recent', 'pub_date', 'participants')
    list_filter = ['pub_date']
    search_fields = ['title']

###### WORDCLOUD #####

class WordCloudChoiceInline(admin.TabularInline):
    model = WordCloudChoice
    extra = 2

class WordCloudAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['featured','is_public']}),
        ('Question Information', {'fields': ['title', 'desc']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    inlines = [WordCloudChoiceInline]
    list_display = ('title', 'is_public', 'recent', 'pub_date', 'participants')
    list_filter = ['pub_date']
    search_fields = ['title']

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Quizz, QuizzAdmin)
admin.site.register(WordCloud, WordCloudAdmin)
