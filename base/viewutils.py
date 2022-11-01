from django.urls import path
from django.shortcuts import render

from django.core.paginator import Paginator
from django.utils.decorators import classonlymethod
# from django.template.response import TemplateResponse
from enum import Enum

#    path('base/cidades/json', views.get_cidades_json, name='base-get_cidades-json')


ViewMethod = Enum(
    "ViewMethod", ["TREE", "LIST", "FORM", "KANBAN", "DIAGRAM", "CALENDAR", "PLANE", "CHART", "MAPS"]
)

class ReverseViews:
    def __init__(self, type, url):
        self.url = url
        self.type = type
    def get_icon(self):
        if self.type == ViewMethod.LIST:
            return "fa-solid fa-bars"
        elif self.type == ViewMethod.TREE:
            return "fa-solid fa-list"
        elif self.type == ViewMethod.KANBAN:
            return "fa-solid fa-address-book"
        elif self.type == ViewMethod.FORM:
            return "fa-regular fa-file"
        elif self.type == ViewMethod.DIAGRAM:
            return "fa-solid fa-diagram-project"
        elif self.type == ViewMethod.MAPS:
            return "fa-solid fa-map-location-dot"
        elif self.type == ViewMethod.CALENDAR:
            return "fa-regular fa-calendar"
        elif self.type == ViewMethod.PLANE:
            return "fa-solid fa-battery-quarter"
        elif self.type == ViewMethod.CHART:
            return "fa-solid fa-chart-pie"

class DefaultViewMode:
    def __init__(self):
        self.model = None
        self.module_name = ''
        self.app_name = ''
        self.views = []
        self.form = None

    def all(self):
        return self.model.objects.all()
    def filter(self, *args, **kwargs):
        return self.model.objects.filter(*args, **kwargs)

    def get_default_context(self, view=ViewMethod.LIST, context={}):
        context["reverse_urls"] = self.views
        if view==ViewMethod.LIST:
            context['objects'] = self.all()
        context['type'] = view
        return context


    def process_request_list(self, request):
        # se tiver alguma query diferente na url
        context = {'objects':self.all(), "reverse_urls":self.views}
        context['type'] = ViewMethod.LIST
        return context
    def getPaginator(self, objects, limit=50, pagina=1):
        return Paginator(objects, limit).get_page(pagina)

    def process_request_form(self, request, pk=0, file=False):
        context = self.get_default_context(view=ViewMethod.FORM)
        if file and pk:
            context['form'] = self.form(request.POST, request.FILES, instance=self.model.objects.get(pk=pk) )
        elif file and not pk:
            context['form'] = self.form(request.POST, request.FILES)
        elif not file and pk:
            context['form'] = self.form(request.POST, instance=self.model.objects.get(pk=pk) )
        elif not file and not pk:
            context['form'] = self.form(request.POST)
        return context

    @classonlymethod
    def tree(ViewMode):
        vw = ViewMode()
        def view_action(request):
            return render(request, vw.module_name+'tree.html', vw.get_default_context())
        return view_action
    @classonlymethod
    def list(cls, **initkwargs):
        def view(request):
            self = cls(**initkwargs)
            if request.GET:
                context = self.process_request_list(request)
            else:
                context = self.get_default_context()
            # context['type'] = ViewMethod.LIST
            return render(request, self.module_name+'list.html', context)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        return view
    @classonlymethod
    def form(cls, create=False):
        if create:
            def view(request):
                self = cls()
                if request.POST:
                    context = self.process_request_form(request)
                    if (type(context)!=dict):
                        return context
                else:
                    if self.form:
                        context = self.get_default_context(view=ViewMethod.FORM, context={"form":self.form()})
                    else:
                        context = self.get_default_context(view=ViewMethod.FORM)
                return render(request, self.module_name+'form.html', context)
        else:
            def view(request, pk):
                self = cls()
                if request.POST:
                    context = self.process_request_form(request, pk=pk)
                    if (type(context)!=dict):
                        return context
                else:

                    if self.form:
                        context = self.get_default_context(view=ViewMethod.FORM, context={'pk':pk, "form":self.form(instance=self.model.objects.get(pk=pk))})
                    else:
                        context = self.get_default_context(view=ViewMethod.FORM)
                return render(request, self.module_name+'form.html', context)
        
        view.view_class = cls

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        return view
    @classonlymethod
    def page(cls, **initkwargs):
        def view(request, pk):
            self = cls(**initkwargs)
            if request.POST:
                context = self.process_request_form(request, pk=pk)
                if (type(context)!=dict):
                    return context
            else:
                context = self.get_default_context(view=ViewMethod.FORM, context={'pk':pk})
                context['object'] = self.model.objects.get(pk=pk)
                # context['type'] = ViewMethod.FORM
            return render(request, self.module_name+'page.html', context)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        return view