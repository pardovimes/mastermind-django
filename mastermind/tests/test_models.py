from django.test import TestCase
from django.db.utils import IntegrityError
from mastermind.models import Game, GuessPeg, Code, Peg


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
        self.assertEqual(game.difficulty, game.secret_code.pegs.count())

    def test_historic_on_game(self):
        game = Game.objects.create()
        user_code = game.generate_random_code()
        self.assertEqual(0, len(game.move_history()))
        feedback_pegs = game.compute_guess(user_code)
        self.assertEqual(1, len(game.move_history()))
        feedback_pegs = game.compute_guess(user_code)
        self.assertEqual(2, len(game.move_history()))
        feedback_pegs = game.compute_guess(user_code)
        self.assertEqual(3, len(game.move_history()))

class CodeModelTest(TestCase):

    def setUp(self):
        self.game = Game.objects.create()

    def test_compare_two_codes_with_different_length(self):
        
        guess_pegs = []
        for i in range(self.game.difficulty + 1):
            guess_pegs.append(GuessPeg.objects.create(
                position=i
            ))
        incremented_code = Code.objects.create()
        incremented_code.pegs.set(guess_pegs)
        user_code = self.game.generate_random_code()
        with self.assertRaises(Exception):
            feedback_pegs = incremented_code.compare_code(user_code)

    def test_compare_two_random_codes(self):
        user_code = self.game.generate_random_code()
        feedback_pegs = self.game.compute_guess(user_code)

    def test_compare_two_equal_codes(self):
        user_code = self.game.generate_random_code()
        feedback_pegs = user_code.compare_code(user_code)
        
        for feedback_peg in feedback_pegs:
        	self.assertEqual(feedback_peg.color, Peg.BLACK)
        
