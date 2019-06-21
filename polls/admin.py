from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'number_of_choices')

    fieldsets = [
        (None, {
            'fields': ['question_text']
        }),
        ('Date Information', {
            'fields': ['pub_date']
        })
    ]

    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)
