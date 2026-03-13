from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def restaurantes(request):
    return render(request, 'restaurantes.html')