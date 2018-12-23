from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from mastermind.models import Game, Move

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

        pegs = request.POST.get('pegs')
        code = []

        for peg in pegs:
     	    code.append(GuessPeg.objects.create(
                position=i
            ))

        game.compute_guess(code)

        return JsonResponse({
            'move': move
        }, status=201)

    moves = list(Move.objects.filter(
                game=game
            ).order_by('pk').values())
    return JsonResponse({
        'moves': moves
    }, status=200)