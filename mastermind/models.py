from django.db import models
from django.db import models
    
class Peg(models.Model):

    BLACK = 'black'
    WHITE = 'white'  
    RED = '#FF0000'
    BLUE = '#0000FF'
    GREEN = '#00FF00'
    YELLOW = '#FFFF00'
    COLORS = (
        (BLACK, '#000'),
        (WHITE, '#FFF'),
        (RED, 'red'),
        (BLUE, 'blue'),
        (GREEN, 'green'),
        (YELLOW, 'yellow'),
    )
    
    color = models.CharField(max_length=10, choices=COLORS)
    position = models.IntegerField(default=0)

class FeedbackPeg(Peg):
	pass

class GuessPeg(Peg):

    def save(self, *args, **kwargs):
        self.color = self.RED
        super().save(*args, **kwargs)


class Code(models.Model):

    pegs = models.ManyToManyField(Peg)

    def compare_code(self, other_code):
        # TODO
        pass


class Game(models.Model):

    EASY = 3
    MEDIUM = 4
    HARD = 5
    INSANE = 101
    DIFFICULTY = (
        (EASY, 'Fácil'),
        (MEDIUM, 'Medio'),
        (HARD, 'Difícil'),
        (INSANE, 'Muy difícil'),
    )

    username = models.CharField(max_length=50)
    difficulty = models.IntegerField(default=MEDIUM)
    secret_code = models.ForeignKey(Code, related_name='games', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.secret_code = self.generate_random_code()
        super().save(*args, **kwargs)

    def get_historical(self):
        # TODO
        pass

    def generate_random_code(self):
        guess_pegs = []
        for i in range(self.difficulty):
        	guess_pegs.append(GuessPeg.objects.create())
        code = Code.objects.create()
        code.pegs.set(guess_pegs)
        return code