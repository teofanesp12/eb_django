from django.shortcuts import render, get_object_or_404

from . import models

# Create your views here.
def home(request):
    context = {'turmas':models.TipoTurma.objects.all}
    return render(request, 'index.html', context)

def turma(request, turma_id):
    turma = get_object_or_404(models.TipoTurma, pk=turma_id)
    materias = models.Materia.objects.filter(tipo_turma=turma)
    return render(request, 'TipoTurma.html', {'turma':turma, 'materias':materias})

def materia(request, materia_id):
    materia = get_object_or_404(models.Materia, pk=materia_id)
    objetivos = models.Objetivo.objects.filter(materia=materia)
    return render(request, 'Materia.html', {'materia':materia, 'objetivos':objetivos})

tecnicas = [
    'Palestra', 'Demonstração', 'Exercício individual', 'Interrogatório', 'Estudo Individual', 'Estudo Dirigido',
    'Estudo Por Meio de Fichas', 'Estudo em computador', 'Discussão dirigida', 'Estudo de caso', 'Estudo Preeliminar',
    'Exercicio militar'
]
from militares.models import Unidade
def objetivo(request, objetivo_id):
    objetivo = get_object_or_404(models.Objetivo, pk=objetivo_id)
    assuntos = models.Assunto.objects.filter(objetivo=objetivo)
    for assunto in assuntos:
        assunto.subassunto = models.SubAssunto.objects.filter(assunto=assunto)
    arquivos = models.FileDoc.objects.filter(objetivo=objetivo)
    context = {'objetivo':objetivo, 'assuntos':assuntos, 'arquivos':arquivos, 'tecnicas':tecnicas}
    context['batalhoes'] = Unidade.objects.all()
    return render(request, 'Objetivo.html', context)

def gerar_plano_session(request, objetivo_id):
    context = {}
    objetivo = get_object_or_404(models.Objetivo, pk=objetivo_id)
    context["assuntos"] = [get_object_or_404(models.Assunto, pk=x) for x in request.POST.getlist('assunto[]') ] 
    context['OM']  =  get_object_or_404(Unidade, pk=request.POST.get('OM', 1))
    context['GDH'] = request.POST.get('GDH', 'Conforme QTS.')
    if not context["GDH"]:
        context['GDH'] = 'Conforme QTS.'
    context['fase']    = request.POST.get('fase', '')
    context['turma']   = request.POST.get('turma', '')
    context['materia'] = objetivo.materia.nome
    context['periodo'] = objetivo.materia.tipo_turma.nome
    context['objetivo'] = request.POST.get('objetivo', '')
    context['intermediario'] = request.POST.get('intermediario', '')
    context['local'] = request.POST.get('local', '')
    context['mai'] = request.POST.get('mai', '')
    context['instrutores'] = request.POST.get('Instrutores', '')
    context['monitores'] = request.POST.get('Monitores', '')
    context['auxiliares'] = request.POST.get('Auxiliares', '')
    context['MAdm'] = request.POST.get('MAdm', '')
    context['MSeg'] = request.POST.get('MSeg', '')
    context['FCons'] = request.POST.get('FCons', '')
    context['CmtSU'] = request.POST.get('CmtSU', '')
    context['S3'] = request.POST.get('S3', '')
    if context['instrutores'].split('\n'):
        context["instrutor"] = context['instrutores'].split('\n')[0]
        context["instrutor"] = context["instrutor"].replace('-', '')
    tcs = request.POST.getlist('tecnica[]')
    context["tecnicas"] = ""
    for t in tcs:
        if context["tecnicas"]:
            context["tecnicas"] += ", "+tecnicas[int(t)]
        else:
            context["tecnicas"] = tecnicas[int(t)]
    # raise Exception(request.POST.getlist('tecnica[]'))
    context['tempo_introducao'] = request.POST.get('tempo_introducao', '')
    context['introducao'] = request.POST.get('introducao', '')
    context['objetivos'] = request.POST.get('objetivos', '')
    context['sumario'] = request.POST.get('sumario', '')
    context['incentivos'] = request.POST.get('incentivos', '')
    context['desenvolvimentos'] = request.POST.get('desenvolvimento', '').split('<div>{nova_pagina}</div>')
    context['tempo_desenvolvimento'] = request.POST.get('tempo_desenvolvimento', '')
    context['conclusao'] = request.POST.get('conclusao', '')
    context['tempo_conclusao'] = request.POST.get('tempo_conclusao', '')
    return render(request, 'plano_session.html', context)


from .models import FatorRisco
def gerenciamento_risco(request, objetivo_id):
    if request.POST:
        if request.POST.get('_popup'):
            fator = FatorRisco()
            fator.nome = request.POST.get('nome_fator')
            fator.probabilidade = int(request.POST.get('probabilidade'))
            fator.gravidade = request.POST.get('gravidade')
            fator.tipo = request.POST.get('tipo')
            fator.objetivo = get_object_or_404(models.Objetivo, pk=objetivo_id)
            fator.save()
        else:
            # Imprimimos...
            pass
    context = {
        'operacional':[],
        'operacional_residual':[],
        'humano':[],
        'humano_residual':[],
        'material':[],
        'material_residual':[],
    }
    context['objetivo_id'] = objetivo_id
    fatores = FatorRisco.objects.filter(objetivo=objetivo_id)
    for fator in fatores:
        if fator.tipo == 'operacional':
            if fator.mitigadora:
                context['operacional_residual'].append(fator)
            else:
                context['operacional'].append(fator)
        elif fator.tipo == 'humano':
            if fator.mitigadora:
                context['humano_residual'].append(fator)
            else:
                context['humano'].append(fator)
        elif fator.tipo == 'material':
            if fator.mitigadora:
                context['material_residual'].append(fator)
            else:
                context['material'].append(fator)

    return render(request, 'gerenciamento_risco.html', context)
def gerenciamento_risco_report(request, objetivo_id):
    return render(request, 'gerenciamento_risco_report.html', {})