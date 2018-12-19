from django.shortcuts import render, redirect

def index(request):
    cookie = False
    if cookie:
        return redirect('game')

    return render(request, 'index.html')

# TODO create decorator - if not cookie escape
def game(request):
    return render(request, 'game.html')