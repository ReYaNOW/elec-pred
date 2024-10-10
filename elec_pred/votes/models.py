from django.conf import settings
from django.db import models
from django.utils import timezone

REASONABLE_LENGTH_TO_DISPLAY = 20


class Question(models.Model):
    question_text = models.CharField('Текст голосования', max_length=200)
    start_date = models.DateTimeField('Дата начала', default=timezone.now)
    end_date = models.DateTimeField('Дата окончания')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Последние голосования будут наверху
        verbose_name = 'Голосование'  # Название в единственном числе
        verbose_name_plural = 'Голосования'  # Название во множественном числе

    def __str__(self):
        return self.question_text

    def total_votes(self) -> int:
        # Подсчитываем общее количество голосов за все варианты этого вопроса
        return Vote.objects.filter(question=self).count()

    @property
    def is_active(self) -> bool:
        return self.start_date <= timezone.now() <= self.end_date


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Голосование'
    )
    choice_text = models.CharField('Текст Выбора', max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Выбор'  # Название в единственном числе
        verbose_name_plural = 'Выборы'  # Название во множественном числе

    def __str__(self):
        question_text = self.question.question_text
        if len(question_text) > REASONABLE_LENGTH_TO_DISPLAY:
            question_text = (
                question_text[:REASONABLE_LENGTH_TO_DISPLAY] + '...'
            )

        return f'{self.choice_text} (Question: {question_text})'

    def get_vote_count(self) -> int:
        # Подсчитываем количество голосов за данный выбор
        return Vote.objects.filter(choice=self).count()

    def get_vote_percentage(self) -> int | float:
        total_votes = (
            self.question.total_votes()
        )  # Общее количество голосов для вопроса
        if total_votes == 0:
            return 0
        return (self.get_vote_count() / total_votes) * 100


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')

    def __str__(self):
        return (
            f'{self.user.username} voted for {self.choice.choice_text} in '
            f'{self.question.question_text}'
        )
