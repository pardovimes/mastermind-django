from django.test import TestCase
from django.db.utils import IntegrityError
from mastermind.models import Game


class GameModelTest(TestCase):

    def test_create_game(self):
        games_created = Game.objects.all()
        number_of_games = len(games_created)
        self.assertEqual(number_of_games, games_created.count())
        game = Game.objects.create()
        games_created = Game.objects.all()
        self.assertEqual(number_of_games + 1, games_created.count())

    def test_number_pegs_on_random_code_creation(self):
        game = Game.objects.create()
        self.assertEqual(4, game.secret_code.pegs.count())