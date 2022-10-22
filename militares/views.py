from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.

from .models import Militar, Graduacao
from .models import Unidade, SubUnidade, Pelotao, GrupoCombate
from base.models import Escolaridade, Religiao
from boletin.models import BoletinDocumento

from access.decorators import login_access_required

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
@login_access_required
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
        messages.add_message(request, messages.SUCCESS, 'Salvo com Sucesso!')
    else:
        form = MilitarForm(instance=instance)
        # messages.add_message(request, messages.INFO, 'Hello world.')

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
            messages.add_message(request, messages.SUCCESS, 'Salvo com Sucesso!')
            return redirect(form.instance)
        else:
            context['form'] = form
            messages.add_message(request, messages.WARNING, 'Confira as suas informações!')
            return render(request, 'militares/militar_edit.html', context)
    context = {}
    form = MilitarForm()
    context['form'] = form
    return render(request, 'militares/militar_edit.html', context)
# LoginRequiredMixin
class MilitarDetailView(generic.DetailView):
    model = Militar
    def get_context_data(self, **kwargs):
        context = super(MilitarDetailView, self).get_context_data(**kwargs)
        context['boletins'] = BoletinDocumento.objects.all()
        return context

    @login_access_required
    def get(self, request, *args, **kwargs):
        return super(MilitarDetailView, self).get(request)

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

#
# Mapa da Força
#
class normal(object):
    def __init__(self):
        self.instance = None
        self.filhos = []
        self.militares = []
    def tipo(self):
        if type(self.instance) == SubUnidade:
            return "subunidade_id"
        elif type(self.instance) == Pelotao:
            return "pelotao_id"
        elif type(self.instance) == GrupoCombate:
            return "gc_id"
        else:
            return "unidade_id"

def getPaginator(militares, limit=50, pagina=1):
    return Paginator(militares, limit).get_page(pagina)

def get_gcs(pelotao_id):
    filhos = []
    for g in GrupoCombate.objects.filter(pelotao=pelotao_id):
        g0 = normal()
        g0.instance  = g
        g0.militares = Militar.objects.filter(grupo_combate=g.pk)
        filhos.append(g0)
    return filhos
def get_pelotoes(subunidade_id):
    filhos = []
    for p in Pelotao.objects.filter(subunidade=subunidade_id):
        p0 = normal()
        p0.instance = p
        p0.militares = Militar.objects.filter(grupo_combate=None, pelotao=p)
        p0.filhos = get_gcs(p.pk)
        filhos.append(p0)
    return filhos
def get_subunidades(unidade_id):
    filhos = []
    for s in SubUnidade.objects.filter(unidade=unidade_id):
        s0 = normal()
        s0.instance  = s
        s0.militares = Militar.objects.filter(grupo_combate=None, pelotao=None, subunidade=s)
        s0.filhos    = get_pelotoes(s.pk)
        filhos.append(s0)
    return filhos
def get_default_context(request):
    context = {}
    context["objects"] = []
    limit = 50
    if request.GET:
        pagina = request.GET.get('pagina',0)
        subunidade_id = request.GET.get('subunidade_id')
        pelotao_id = request.GET.get('pelotao_id')
        gc_id = request.GET.get('gc_id')
        if subunidade_id:
            res = normal()
            su = SubUnidade.objects.get(pk=request.GET.get('subunidade_id'))
            res.instance = su
            res.filhos   = Pelotao.objects.filter(subunidade=su)
            res.militares = [x for x in Militar.objects.filter(subunidade=su, pelotao=None)]
            for pel in res.filhos:
                res.militares += Militar.objects.filter(pelotao=pel)
            res.militares = getPaginator(res.militares, limit=limit, pagina=pagina)
            context["tipo"] = "pelotao_id"
            context["objects"].append(res)
        if pelotao_id:
            res = normal()
            pel = Pelotao.objects.get(pk=request.GET.get('pelotao_id'))
            res.instance = pel
            res.filhos   = GrupoCombate.objects.filter(pelotao=pel)
            res.militares = [x for x in Militar.objects.filter(pelotao=pel, grupo_combate=None)]
            for gc in res.filhos:
                res.militares += Militar.objects.filter(grupo_combate=gc)
            res.militares = getPaginator(res.militares, limit=limit, pagina=pagina)
            context["tipo"] = "gc_id"
            context["objects"].append(res)
        if gc_id:
            res = normal()
            gc = GrupoCombate.objects.get(pk=request.GET.get('gc_id'))
            res.instance    = gc
            res.militares = getPaginator(Militar.objects.filter(grupo_combate=gc), limit=limit, pagina=pagina)
            context["tipo"] = "militares"
            context["objects"].append(res)
        if not subunidade_id and not pelotao_id and not gc_id:
            for u in Unidade.objects.all():
                res = normal()
                res.instance = u
                res.filhos   = SubUnidade.objects.filter(unidade=u)
                for su in res.filhos:
                    res.militares += Militar.objects.filter(subunidade=su)
                res.militares = getPaginator(res.militares, limit=limit, pagina=pagina)
                context["tipo"] = "subunidade_id"
                context["objects"].append(res)
    else:
        for u in Unidade.objects.all():
            res = normal()
            res.instance = u
            res.filhos   = SubUnidade.objects.filter(unidade=u)
            for su in res.filhos:
                res.militares += Militar.objects.filter(subunidade=su)
            res.militares = getPaginator(res.militares, limit=limit)
            context["tipo"] = "subunidade_id"
            context["objects"].append(res)
    return context
@login_required
def map_force_tree(request):
    context = {}
    context["unidades"] = []
    if request.GET:
        subunidade_id = request.GET.get("subunidade_id")
        pelotao_id = request.GET.get("pelotao_id")
        gc_id = request.GET.get("gc_id")
        if subunidade_id:
            res = normal()
            res.instance = SubUnidade.objects.get(pk=subunidade_id)
            res.filhos = get_pelotoes(subunidade_id)
            context["unidades"] = [res]
        elif pelotao_id:
            res = normal()
            res.instance = Pelotao.objects.get(pk=pelotao_id)
            res.filhos = get_gcs(pelotao_id)
            context["unidades"] = [res]
        elif gc_id:
            res = normal()
            res.instance = GrupoCombate.objects.get(pk=gc_id)
            # res.filhos = get_gcs(pelotao_id)
            res.militares = Militar.objects.filter(grupo_combate=res.instance)
            context["unidades"] = [res]
    else:
        for b in Unidade.objects.all():
            b0 = normal()
            b0.instance = b
            b0.filhos = get_subunidades(b.pk)
            context["unidades"].append(b0)
    return render(request, 'militares/mapforce/tree.html', context)
@login_required
def map_force_list(request):
    context = get_default_context(request)
    return render(request, 'militares/mapforce/list.html', context)
@login_required
def map_force_kanban(request):
    context = get_default_context(request)
    return render(request, 'militares/mapforce/kanban.html', context)
@login_required
def map_force_maps(request):
    context = get_default_context(request)
    return render(request, 'militares/mapforce/maps.html', context)
@login_required
def map_force_diagram(request):
    context = {}

    return render(request, 'militares/mapforce/diagram.html', context)

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