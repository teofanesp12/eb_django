from django.shortcuts import render

# Create your views here.
from .models import CategoriaConteudoAtitudinal, ConteudoAtitudinal

def home(request):
    context = {}
    categorias = CategoriaConteudoAtitudinal.objects.filter()
    conteudos  = ConteudoAtitudinal.objects.filter()
    context['categorias'] = categorias
    context['conteudos']  = conteudos
    return render(request, 'ndaca/home.html', context)