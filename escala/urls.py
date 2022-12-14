"""exercito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'escala'

urlpatterns = [
    path('', views.home, name='home'),

    # Serviço Escala
    path('servicoescala/', views.ServicoEscalaView.list(), name='view-servicoescala-list'),
    path('servicoescala/adicionar', views.ServicoEscalaView.form(create=True), name='view-servicoescala-form'),
    
    # Serviço Local
    path('servicolocal/', views.ServicoLocalView.list(), name='view-servicolocal-list'),
    path('servicolocal/adicionar', views.ServicoLocalView.form(create=True), name='view-servicolocal-form'),
    path('servicolocal/<int:pk>/editar', views.ServicoLocalView.form(), name='view-servicolocal_editar-form'),
    path('servicolocal/<int:pk>/', views.ServicoLocalView.page(), name='view-servicolocal-page'),
]