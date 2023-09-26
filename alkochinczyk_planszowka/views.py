from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View

from alkochinczyk_planszowka.constants.view_names import GAME_DETAIL_VIEW_NAME
from alkochinczyk_planszowka.forms import GameForm, TransactionForm
from alkochinczyk_planszowka.models import Account, Game, Player, Transaction

class IndexView(generic.ListView):
    template_name = 'alkochinczyk/ind.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.all().order_by("-id")


class GameDetailView(View):
    form_class = Transaction
    template_name = 'alkochinczyk/detal.html'

    def get(self, request, game_id):
        return render(request, self.template_name, self.get_game_context(game_id))

    def post(self, request, game_id):
        form = Transaction(game_id, request.POST)
        if form.is_valid():
            transaction = form.save()
            return redirect(GAME_DETAIL_VIEW_NAME, game_id)
        else:
            return render(request, self.template_name, self.get_game_context(game_id, form))

    def get_game_context(self, game_id, form=None):
        return {
            'game_accounts'      : self.get_game_accounts(game_id),
            'form'               : form if form else Transaction(game_id),
            'recent_transactions': self.get_recent_transactions(game_id), }

    # TODO: Memoize
    def get_game_accounts(self, game_id):
        game = get_object_or_404(Game, id=game_id)
        return game.account_set.all()

    # TODO: Reduce the db calls?
    def get_recent_transactions(self, game_id):
        return Transaction.objects.filter(
            payer_account__game_id=game_id,
            payee_account__game_id=game_id).order_by("-id")[:10]


class NewGameView(View):
    form_class = Game
    template_name = 'alkochinczyk/newgame.html'

    def get(self, request):
        context = {
            'form': Game()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        id_players = request.POST.getlist(u'players')

        if id_players:
            new_game = Game()
            new_game.save()

            STARTING_PLAYER_BALANCE = 1500
            STARTING_BANKER_BALANCE = 150000

            for player_id in id_players:
                account = Account()
                account.game = new_game
                account.player = Player.objects.get(id=player_id)
                account.balance = STARTING_PLAYER_BALANCE
                account.save()

            banker = Player.objects.get(person__username='bank')
            banker_account = Account()
            banker_account.game = new_game
            banker_account.player = banker
            banker_account.balance = STARTING_BANKER_BALANCE
            banker_account.save()
            return redirect(GAME_DETAIL_VIEW_NAME, new_game.id)