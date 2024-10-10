from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Choice, Question, Vote


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


# Админка для Vote (Голоса пользователей)
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice', 'created_at')
    list_filter = ('question', 'choice')  # Фильтр по вопросу и выбору
    search_fields = (
        'user__username',
        'question__question_text',
        'choice__choice_text',
    )  # Поиск по пользователю, вопросу и выбору
    actions = ['delete_selected_votes']

    # Возможность удаления выбранных голосов
    def delete_selected_votes(
        self, request: HttpRequest, queryset: QuerySet
    ) -> None:
        deleted_count, _ = queryset.delete()
        self.message_user(request, f'Успешно удалено {deleted_count} голосов.')

    delete_selected_votes.short_description = 'Удалить выбранные голоса'
