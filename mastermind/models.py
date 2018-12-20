from django.db import models
from django.db import models
    
class Peg(models.Model):
    
    RED = '#FF0000'
    BLUE = '#0000FF'
    GREEN = '#00FF00'
    YELLOW = '#FFFF00'
    COLORS = (
        (RED, 'red'),
        (BLUE, 'blue'),
        (GREEN, 'green'),
        (YELLOW, 'yellow'),
    )
    
    color = models.CharField(max_length=10, choices=COLORS)
    position = models.IntegerField(default=0)

class Code(models.Model):

    BLACK = 'black'
    WHITE = 'white'
    KEY_PEGS = (
        (BLACK, '#000'),
        (WHITE, '#FFF'),
    )

    pegs = models.ManyToManyField(Peg)

    def compare_code(self, other_code):
    	# TODO
    	pass


class Game(models.Model):

    username = models.CharField(max_length=50)
    secret_code = models.ForeignKey(Code, related_name='games', on_delete=models.CASCADE)

    def get_historical(self):
    	# TODO
    	pass