from django.db.models import QuerySet
from django.views.generic import ListView

from .models import News

AMOUNT_TO_STORE = 15


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self) -> QuerySet[News]:
        news_queryset = News.objects.all().order_by('-created_at')

        if news_queryset.count() > AMOUNT_TO_STORE:
            ids_to_delete = news_queryset[AMOUNT_TO_STORE:].values_list(
                'id', flat=True
            )
            News.objects.filter(id__in=ids_to_delete).delete()

        return news_queryset
