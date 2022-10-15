from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
# Create your views here.

from .models import Militar, Graduacao, Pelotao, GrupoCombate
from base.models import Escolaridade, Religiao
from boletin.models import BoletinDocumento

from .forms import MilitarForm

import datetime

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=None,
        secure=None,
    )

def edit_militar(request, pk):
    context = {}
    instance=Militar.objects.get(pk=pk)
    if instance.naturalidade:
        context['id_naturalidade_estado'] = instance.naturalidade.estado.pk
        context['id_naturalidade'] = instance.naturalidade.pk
    if instance.cidade_endereco:
        context['id_estado_endereco'] = instance.cidade_endereco.estado.pk
        context['id_cidade_endereco'] = instance.cidade_endereco.pk
    if request.POST:
        form = MilitarForm(request.POST, request.FILES, instance=instance)
        form.save()
    else:
        form = MilitarForm(instance=instance)

    context['form'] = form
    return render(request, 'militares/militar_edit.html', context)

def create_militar(request):
    if request.POST:
        try:
            if request.POST.get('cpf'):
                militar = Militar.objects.get(cpf=request.POST.get('cpf'))
                if militar:
                    return redirect('access:access-login-view')
        except Exception:
            pass
        form = MilitarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(form.instance)
        else:
            context['form'] = form
            return render(request, 'militares/militar_edit.html', context)
    context = {}
    form = MilitarForm()
    context['form'] = form
    return render(request, 'militares/militar_edit.html', context)

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


def get_pelotao_json(request):
    json = {}
    if request.GET:
        subunidade = request.GET.get('subunidade',0)
        if subunidade == '':
            subunidade = 0
        pelotoes    = Pelotao.objects.filter(subunidade=subunidade)
    else:
        pelotoes    = Pelotao.objects.all()
    json['pelotoes'] = [(x.pk,x.nome) for x in pelotoes]
    return JsonResponse(json)

def get_gc_json(request):
    json = {}
    if request.GET:
        pelotao = request.GET.get('pelotao',0)
        if pelotao == '':
            pelotao = 0
        gcs    = GrupoCombate.objects.filter(pelotao=pelotao)
    else:
        gcs    = GrupoCombate.objects.all()
    json['gcs'] = [(x.pk,x.nome) for x in gcs]
    return JsonResponse(json)