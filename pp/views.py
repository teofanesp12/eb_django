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

def gerar_plano_seguranca(request, objetivo_id):
    context = {}
    objetivo = get_object_or_404(models.Objetivo, pk=objetivo_id)
    context["materia"] = objetivo.materia
    context["assuntos"] = [get_object_or_404(models.Assunto, pk=x) for x in request.POST.getlist('assunto[]') ]
    context['OM']  =  get_object_or_404(Unidade, pk=request.POST.get('OM', 1))
    context['finalidade'] = request.POST.get('finalidade')
    context['referencias'] = request.POST.get('referencias').replace('lower-alpha','lower-alpha;padding-left: 20px;')

    context['periodo'] = request.POST.get('periodo')
    context['local'] = request.POST.get('local')
    context['instruendos'] = request.POST.get('instruendos')
    context['equipe_instrucao'] = request.POST.get('equipe_instrucao')
    context['condicoes_execucao'] = request.POST.get('condicoes_execucao')
    context['grau_risco'] = request.POST.get('grau_risco')
    context['medidas_preventivas'] = request.POST.get('medidas_preventivas')
    context['normas_gerais'] = request.POST.get('normas_gerais')
    context['medidas_particulares'] = request.POST.get('medidas_particulares')
    context['medidas_caso_acidente'] = request.POST.get('medidas_caso_acidente').replace('lower-alpha','lower-alpha;padding-left: 20px;')
    context['comunicacao'] = request.POST.get('comunicacao')
    context['rec_ensaio_briefing'] = request.POST.get('rec_ensaio_briefing')
    context['medidas_outras'] = request.POST.get('medidas_outras')

    context['instrutor'] = request.POST.get('instrutor')
    context['opai'] = request.POST.get('opai')
    return render(request, 'plano_seguranca.html', context)

from .models import FatorRisco
def action_get_class_risco(probabilidade=0, gravidade='A', result_type=0):
    if result_type==0:
        result=['Inaceitavel', 'Muito Alto', 'Alto', 'Medio', 'Baixo']
    elif result_type==1:
        result=['background: black;color: white;', 'background-color: red;color: white;', 'background-color: yellow;', 'background-color: #6ec32a;', 'background-color: green;color: white;']
    if probabilidade == 5:
        if gravidade=='A':
            return result[0]# 'inaceitavel'
        elif gravidade in ['B','C']:
            return result[1]# 'muito_alto'
        elif gravidade=='D':
            return result[2]# 'alto'
        elif gravidade=='E':
            return result[3]# 'Medio'
    elif probabilidade == 4:
        if gravidade in ['A','B']:
            return result[1]
        elif gravidade in ['C']:
            return result[2]
        elif gravidade in ['D','E']:
            return result[3]
    elif probabilidade == 3:
        if gravidade in ['A']:
            return result[1]
        elif gravidade in ['B']:
            return result[2]
        elif gravidade in ['C']:
            return result[3]
        elif gravidade in ['D','E']:
            return result[4]
    elif probabilidade == 2:
        if gravidade in ['A']:
            return result[2]
        elif gravidade in ['B','C']:
            return result[3]
        elif gravidade in ['D','E']:
            return result[4]
    elif probabilidade == 1:
        return result[4]
    return '-'
def gerenciamento_risco(request, objetivo_id):
    if request.POST:
        if request.POST.get('_popup'):
            if request.POST.get('fator_pk'):
                fator = FatorRisco.objects.get(pk=request.POST.get('fator_pk'))
                fator.probabilidade_residual = int(request.POST.get('probabilidade_residual',0))
                fator.gravidade_residual = request.POST.get('gravidade_residual')
                fator.mitigadora = request.POST.get('mitigadora')
            else:
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
    probabilidade_antes  = []
    probabilidade_depois = []
    gravidade_antes      = []
    gravidade_depois     = []
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

        probabilidade_antes.append(fator.probabilidade)
        gravidade_antes.append(fator.gravidade)
        if fator.mitigadora:
            probabilidade_depois.append(fator.probabilidade_residual)
            gravidade_depois.append(fator.gravidade_residual)
        else:
            probabilidade_depois.append(fator.probabilidade)
            gravidade_depois.append(fator.gravidade)
    probabilidade_antes.sort()
    probabilidade_antes.reverse()
    probabilidade_depois.sort()
    probabilidade_depois.reverse()
    gravidade_antes.sort()
    gravidade_depois.sort()
    context['probabilidade_antes']  = len(probabilidade_antes)>=1 and probabilidade_antes[0] or '-'
    context['probabilidade_depois'] = len(probabilidade_depois)>=1 and probabilidade_depois[0] or '-'
    context['gravidade_antes']      = len(gravidade_antes)>=1 and gravidade_antes[0] or '-'
    context['gravidade_depois']     = len(gravidade_depois)>=1 and gravidade_depois[0] or '-'
    context['classe_risco_antes']   = action_get_class_risco(context['probabilidade_antes'], context['gravidade_antes'])
    context['classe_risco_depois']  = action_get_class_risco(context['probabilidade_depois'], context['gravidade_depois'])
    return render(request, 'gerenciamento_risco.html', context)
def gerenciamento_risco_report(request, objetivo_id):
    return render(request, 'gerenciamento_risco_report.html', {})