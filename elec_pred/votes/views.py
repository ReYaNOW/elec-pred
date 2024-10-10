from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .models import Choice, Question, Vote


class ActiveVotesView(LoginRequiredMixin, ListView):
    template_name = 'votes/active_votes.html'
    context_object_name = 'votes'

    def get_queryset(self) -> QuerySet[Question]:
        """Return the active questions."""
        now = timezone.now()
        return Question.objects.filter(start_date__lte=now, end_date__gte=now)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add total votes and user vote information to context."""
        context = super().get_context_data(**kwargs)
        context['total_votes'] = sum(
            question.total_votes() for question in context['votes']
        )

        # Добавляем информацию о том, проголосовал ли пользователь
        for question in context['votes']:
            user_vote = Vote.objects.filter(
                user=self.request.user, question=question
            ).first()
            question.user_vote = user_vote

        return context


class VoteView(LoginRequiredMixin, View):
    def post(
        self, request: HttpRequest, question_id: int
    ) -> HttpResponseRedirect:
        """Handle voting."""
        question = get_object_or_404(Question, pk=question_id)

        # Проверяем, голосовал ли пользователь за этот вопрос
        existing_vote = Vote.objects.filter(
            user=request.user, question=question
        ).first()
        if existing_vote:
            messages.error(
                self.request, 'Вы уже участвовали в этом голосовании'
            )
            return redirect('active_votes')

        # Получаем выбранный вариант ответа
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)

        # Создаем новый голос
        Vote.objects.create(
            user=request.user, question=question, choice=choice
        )

        messages.success(self.request, 'Ваш ответ принят')
        # Перенаправляем на активные голосования
        return redirect('active_votes')


class PastVotesView(LoginRequiredMixin, ListView):
    template_name = 'votes/past_votes.html'
    context_object_name = 'votes'

    def get_queryset(self) -> QuerySet[Question]:
        """Return the past questions."""
        return Question.objects.filter(end_date__lt=timezone.now())
