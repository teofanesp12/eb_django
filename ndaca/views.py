from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from .models import CategoriaConteudoAtitudinal, ConteudoAtitudinal

def home(request):
    context = {}
    categorias = CategoriaConteudoAtitudinal.objects.filter()
    conteudos  = ConteudoAtitudinal.objects.filter()
    context['categorias'] = categorias
    context['conteudos']  = conteudos
    return render(request, 'ndaca/home.html', context)


def get_conteudo_atitudinal_json(request):
    json = {}
    if request.GET:
        pk = request.GET.get("pk")
        conteudo    = ConteudoAtitudinal.objects.get(pk=pk)
        json['detalhes'] = conteudo.detalhes or ""
        json['exemplos'] = conteudo.exemplos or ""
    return JsonResponse(json)