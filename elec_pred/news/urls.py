from django.urls import path

from elec_pred.news.views import NewsListView

urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
]
