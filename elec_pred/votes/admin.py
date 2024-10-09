from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'start_date', 'end_date', 'is_active')
    inlines = [ChoiceInline]

    @admin.display(description='Статус голосования')
    def is_active(self, obj: Question) -> bool:
        return obj.is_active

    is_active.boolean = True


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text')
