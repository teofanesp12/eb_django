from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from .models import Militar, Graduacao
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
    if request.POST:
        form = MilitarForm(request.POST, instance=Militar.objects.get(pk=pk))
        form.save()
    else:
        form = MilitarForm(instance=Militar.objects.get(pk=pk))

    context['form'] = form
    return render(request, 'militares/militar_edit.html', context)

def create_militar(request):
    if request.POST:
        form = MilitarForm(request.POST)
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