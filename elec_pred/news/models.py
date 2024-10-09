from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Последние новости будут наверху
        verbose_name = 'Новость'  # Название в единственном числе
        verbose_name_plural = 'Новости'  # Название во множественном числе

    def __str__(self):
        return self.title
