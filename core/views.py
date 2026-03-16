from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def restaurantes(request):
    return render(request, 'restaurantes.html')

def menu_beer(request):
    return render(request, 'menu_beer.html')

def menu_taqueria(request):
    return render(request, 'menu_taqueria.html')

def burgers(request):
    return render(request, 'burgers.html')

def entradas(request):
    return render(request, 'entradas.html')

def comidas_rapidas(request):
    return render(request, 'comidas_rapidas.html')

def especiales_beer(request):
    return render(request, 'especiales_beer.html')

def picadas(request):
    return render(request, 'picadas.html')

def bebidas(request):
    return render(request, 'bebidas.html')

def taco_carne(request):
    return render(request, 'taco_carne.html')

def dorilocos(request):
    return render(request, 'dorilocos.html')

def picadas_mexicanas(request):
    return render(request, 'picadas_mexicanas.html')

def burritos(request):
    return render(request, 'burritos.html')

def maruchas(request):
    return render(request, 'maruchas.html')