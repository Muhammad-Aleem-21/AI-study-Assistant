from django.contrib import admin

# Register your models here.

from .models import Note, Summary, Quiz, Question, Choice

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "content")

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("note",)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("note", "created_at")

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
