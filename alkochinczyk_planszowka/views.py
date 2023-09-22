from django.shortcuts import render
from .models import Place, Player, ChanceCard, CommunityChestCard

def board_view(request):
    board = [[i + j * 11 for i in range(11)] for j in range(11)]
    players = Player.objects.all()
    places = Place.objects.all()
    chance_cards = ChanceCard.objects.all()
    community_chest_cards = CommunityChestCard.objects.all()

    context = {
        'board': board,
        'players': players,
        'places': places,
        'chance_cards': chance_cards,
        'community_chest_cards': community_chest_cards,
    }

    return render(request, 'alkochinczyk/board_view.html', context)