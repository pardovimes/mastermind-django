from django.test import TestCase
from mastermind.models import Game, GuessPeg, Code, Peg
from django.urls import reverse

class GameModelTest(TestCase):

    def test_game_get(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)


    def test_game_post(self):
        games_created = Game.objects.all()
        number_of_games = len(games_created)
        self.assertEqual(number_of_games, games_created.count())
        response = self.client.post(reverse('games'))
        self.assertEqual(response.status_code, 201)
        games_created = Game.objects.all()
        self.assertEqual(number_of_games + 1, games_created.count())

class MoveModelTest(TestCase):

    def setUp(self):
        self.game = Game.objects.create()

    def test_move_get(self):
        game = Game.objects.all().first()
        response = self.client.get(reverse('make_move', kwargs={'pk':game.pk}))
        self.assertEqual(response.status_code, 200)


    def test_move_post(self template):
        game = Game.objects.all().first()
        response = self.client.post(reverse('make_move', kwargs={'pk':game.pk}), {
            'pegs' : ['red','red','red','red']
        })
        kwargs = template.call_args[1]
        context = kwargs['context']
        print(context['feedback'])

    def test_get_history(self):
        pass