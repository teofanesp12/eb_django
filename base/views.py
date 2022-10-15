from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
	return render(request, 'index_home.html', {})


from .models import Cidade, Estado
def get_estados_json(request):
    json = {}
    json['estados'] = [(x.pk,x.nome) for x in Estado.objects.all()]
    return JsonResponse(json)

def get_cidades_json(request):
    json = {}
    if request.GET:
        id_estado = request.GET.get('id_estado',0)
        if id_estado == '':
            id_estado = 0
        cidades    = Cidade.objects.filter(estado=id_estado)
    else:
        cidades    = Cidade.objects.all()
    json['cidades'] = [(x.pk,x.nome) for x in cidades]
    return JsonResponse(json)