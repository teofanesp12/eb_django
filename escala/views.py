from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from base.viewutils import DefaultViewMode, ViewMethod, ReverseViews

from .models import ServicoLocal, ServicoLocalLinha, ServicoEscala
from .forms import ServicoLocalForm, ServicoLocalLinhaForm, ServicoEscalaForm
# Create your views here.
def home(request):
    context = {}
    return render(request, 'escala/home.html', context)

class ServicoLocalView(DefaultViewMode):
    def __init__(self):
        self.model = ServicoLocal
        self.module_name = 'escala/servicolocal/'

        self.views = [
            ReverseViews(ViewMethod.LIST, reverse('escala:view-servicolocal-list')),
            ReverseViews(ViewMethod.FORM, reverse('escala:view-servicolocal-form')),
            #TODO add Maps Forms
        ]
        self.form = ServicoLocalForm

    def process_request_list(self, request):
        context = super().process_request_list(request)
        pagina  = request.GET.get('pagina', 0)
        limit   = request.GET.get('limit', 50)
        context['objects'] = self.getPaginator(context['objects'], limit=limit, pagina=pagina)
        return context

    def process_request_form(self, request, pk=0, file=False):
        if request.POST.get("popup", None):
            # messages.add_message(request, messages.INFO, 'Teste!')
            form = ServicoLocalLinhaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Adicionado com Sucesso!')
                return redirect(request.build_absolute_uri())
            else:
                messages.add_message(request, messages.WARNING, 'Confira as suas informações!')
            context['linha_form'] = form
        context = super().process_request_form(request, pk=pk, file=False)
        if context['form'].is_valid:
            context['form'].save()
            messages.add_message(request, messages.SUCCESS, 'Salvo com Sucesso!')
        else:
            messages.add_message(request, messages.WARNING, 'Confira as suas informações!')
        return context

    def get_default_context(self, view=ViewMethod.LIST, context={}):
        context = super().get_default_context(view=view, context=context)
        if view==ViewMethod.FORM:
            context['linhas'] = ServicoLocalLinha.objects.filter(local=context.get('pk', 0))
            context['linha_form'] = ServicoLocalLinhaForm()
        return context

class ServicoEscalaView(DefaultViewMode):
    def __init__(self):
        self.model = ServicoEscala
        self.module_name = 'escala/servicoescala/'

        self.views = [
            ReverseViews(ViewMethod.LIST, reverse('escala:view-servicoescala-list')),
            ReverseViews(ViewMethod.FORM, reverse('escala:view-servicoescala-form'))
        ]
        self.form = ServicoEscalaForm

    def process_request_list(self, request):
        context = super().process_request_list(request)
        pagina  = request.GET.get('pagina', 0)
        limit   = request.GET.get('limit', 50)
        context['objects'] = self.getPaginator(context['objects'], limit=limit, pagina=pagina)
        return context