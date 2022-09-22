from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from .models import Militar, Graduacao
from base.models import Escolaridade, Religiao
from boletin.models import BoletinDocumento

class MilitarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Militar
    def get_context_data(self, **kwargs):
        context = super(MilitarDetailView, self).get_context_data(**kwargs)
        context['boletins'] = BoletinDocumento.objects.all()
        return context

def gerate_assentamentos(request, pk):
    context = {}
    militar = Militar.objects.get(pk=pk)
    context['militar'] = militar
    return render(request, 'militares/assentamento_report.html', context)

import random
class Data:
    label = ''
    datas = []
    red   = 255
    green = 255
    blue  = 255
def escolaridade_report(request):
    context = {}
    escolaridade = Escolaridade.objects.all()
    # militares    = Militar.objects.all()
    context['escolaridade'] = escolaridade
    context['datas'] = []
    for graduacao in Graduacao.objects.all():
        militares = Militar.objects.filter(graduacao=graduacao)
        if not militares:
            continue
        d = Data()
        d.label = graduacao.nome
        d.datas = []
        for es in escolaridade:
            d.datas.append( len(militares.filter(escolaridade=es)) )
            d.red = random.randint(0, 255)
            d.green = random.randint(0, 255)
            d.blue = random.randint(0, 255)
        context['datas'].append(d)
    return render(request, 'militares/escolaridade_report.html', context)

def religiao_report(request):
    context = {}
    religiao = Religiao.objects.all()
    context['religiao'] = religiao
    context['datas'] = []
    for graduacao in Graduacao.objects.all():
        militares = Militar.objects.filter(graduacao=graduacao)
        if not militares:
            continue
        d = Data()
        d.label = graduacao.nome
        d.datas = []
        for rel in religiao:
            d.datas.append( len(militares.filter(religiao=rel)) )
            d.red = random.randint(0, 255)
            d.green = random.randint(0, 255)
            d.blue = random.randint(0, 255)
        context['datas'].append(d)
    return render(request, 'militares/religiao_report.html', context)

def geochart_report(request):
    context = {}

    return render(request, 'militares/geochart_militares.html', context)