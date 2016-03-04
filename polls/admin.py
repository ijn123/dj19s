from django.contrib import admin
from .models import Choice, Question


# Register your models here.


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['question_text'] #show only question_text in admin change page . order in which this fields will be display
    # fields = ['pub_date', 'question_text']
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    # list_filter = ['pub_date', 'question_text']
    search_fields = ['question_text']
    #pagination
    list_per_page = 2
    date_hierarchy = 'pub_date'
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
