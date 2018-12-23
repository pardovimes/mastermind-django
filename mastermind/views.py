from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from mastermind.models import Game, Move, GuessPeg, Code

def games(request):

    if request.method == 'POST':
        game = Game.objects.create()
        return JsonResponse({
            'game': game.toJSON()
        }, status=201)

    games = Game.objects.all().order_by('pk')
    games = [game.toJSON() for game in games]
    return JsonResponse({
        'games': games
    }, status=200)

def make_move(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == 'POST':

        if True:
            pegs = request.POST.getlist('pegs')
            code = Code.objects.create()

            for i, peg in enumerate(pegs):
                 code.pegs.add(GuessPeg.objects.create(
                    color=peg,
                    position=i
                ))
            feedback_pegs = game.compute_guess(code)
            
            return JsonResponse({
                'feedback': [str(feedback_peg) for feedback_peg in feedback_pegs]
            }, status=201)
        

            print(e)
            return JsonResponse({
                'message': str(e)
            }, status=500)

    moves = list(Move.objects.filter(
                game=game
            ).order_by('pk').values())
    return JsonResponse({
        'moves': moves
    }, status=200)