from django.urls import path

from alkochinczyk_planszowka.views import NewGameView, GameDetailView, IndexView
from alkochinczyk_planszowka.constants.view_names import GAME_DETAIL_VIEW_NAME, INDEX_VIEW_NAME, NEW_GAME_VIEW_NAME

app_name = 'Alkochinczyk'

urlpatterns = [
    path('', NewGameView.as_view(), name='NEW_GAME_VIEW_NAME'),
    path('', IndexView.as_view(), name='INDEX_VIEW_NAME'),
    path('', GameDetailView.as_view(), name='GAME_DETAIL_VIEW_NAME'),
]
