from django.urls import path

from elec_pred.votes.views import ActiveVotesView, PastVotesView, VoteView

urlpatterns = [
    path('active/', ActiveVotesView.as_view(), name='active_votes'),
    path('past/', PastVotesView.as_view(), name='past_votes'),
    path('vote/<int:question_id>/', VoteView.as_view(), name='vote'),
]
