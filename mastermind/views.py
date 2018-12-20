from django.shortcuts import render, redirect

def index(request):
    cookie = False
    if cookie:
        return redirect('game')

    if request.method == 'POST':
    	username = request.POST.get('username')
    	print(username)
    	return redirect('game')

    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')