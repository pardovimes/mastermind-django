import random
from django.db import models
from django.utils import timezone

class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
        super().save(*args, **kwargs)

class Peg(models.Model):

    BLACK = 'black'
    WHITE = 'white'
    FEEDBACK_COLORS = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
    )
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    COLORS = (
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (GREEN, 'green'),
        (YELLOW, 'yellow'),
    )
    
    color = models.CharField(max_length=10, choices=COLORS, default=RED)
    position = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.color} - {self.position}'

class FeedbackPeg(Peg):
    pass

class GuessPeg(Peg):

    def save(self, *args, **kwargs):
        random_color = random.choice(self.COLORS)[0]
        self.color = random_color
        super().save(*args, **kwargs)


class Code(models.Model):

    pegs = models.ManyToManyField(GuessPeg)

    def compare_code(self, other_code):

        self_pegs = self.pegs.all().order_by('position').values('color')
        other_code_pegs = other_code.pegs.all().order_by('position').values('color')

        if len(self_pegs) != len(other_code_pegs):
            raise Exception("Codes doesn't have the same number of elements")

        feedback_pegs = []

        for i, peg in enumerate(self_pegs):
            self_peg_color = self_pegs[i]
            other_code_peg_color = other_code_pegs[i]
            
            if other_code_peg_color == self_peg_color:
                feedback_pegs.append(FeedbackPeg.objects.create(
                    color=FeedbackPeg.BLACK,
                    position=i
                ))
            elif other_code_peg_color in self_pegs:
                feedback_pegs.append(FeedbackPeg.objects.create(
                    color=FeedbackPeg.WHITE,
                    position=i
                ))

        return feedback_pegs
        

    def __str__(self):
        return ' // '.join(str(e) for e in self.pegs.all().order_by('position'))

class Game(models.Model):

    EASY = 3
    MEDIUM = 4
    HARD = 5
    INSANE = 101
    DIFFICULTY = (
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
        (INSANE, 'Insane'),
    )

    username = models.CharField(max_length=50)
    difficulty = models.IntegerField(default=MEDIUM)
    secret_code = models.ForeignKey(Code, related_name='games', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.secret_code = self.generate_random_code()
        super().save(*args, **kwargs)

    def generate_random_code(self):
        guess_pegs = []
        for i in range(self.difficulty):
            guess_pegs.append(GuessPeg.objects.create(
                position=i
            ))
        code = Code.objects.create()
        code.pegs.set(guess_pegs)
        return code

    def compute_guess(self, guess_code):
        feedback_pegs = self.secret_code.compare_code(guess_code)
        move = Move.objects.create(
            game=self,
            code=guess_code
        )
        move.feedback.set(feedback_pegs)
        return feedback_pegs

class Move(TimeStamped):

    feedback = models.ManyToManyField(FeedbackPeg)
    code = models.ForeignKey(Code, related_name='moves', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='moves', on_delete=models.CASCADE)
