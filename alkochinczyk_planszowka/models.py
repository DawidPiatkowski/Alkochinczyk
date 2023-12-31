from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Player(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person.__str__()


class Game(models.Model):
    players = models.ManyToManyField(Player, through='Account')
    start_time = models.DateTimeField(auto_now=True)

    @property
    def __str__(self):
        return "Game: %s" % str(self.id)


class Account(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    balance = models.IntegerField()

    class Meta:
        unique_together = ('game', 'player',)

    def __str__(self):
        return str(self.player)


class Transaction(models.Model):
    payer_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payer_account')
    payee_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payee_account')
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        msg = "%s paid to %s %d." % (
            self.payer_account.player.person.username,
            self.payee_account.player.person.username,
            self.amount
        )
        if self.description:
            msg += " Remarks: %s" % (self.description)

        return msg

    def clean(self):
        if self.payer_account.balance < self.amount:
            raise ValidationError(
                ('Payer account balance is not sufficient to complete this transaction, short by %d' % (
                        self.amount - self.payer_account.balance)))

        if self.payer_account.id == self.payee_account_id:
            raise ValidationError(('Payer and payee account must not be same'))

        if self.amount == 0:
            raise ValidationError(('Transaction amount can not be zero'))
