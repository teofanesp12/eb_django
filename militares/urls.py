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

app_name = 'militar'

urlpatterns = [
    # path('', views.home, name='home'),
    path('militares/adicionar/', views.create_militar, name='militar-create_militar-view'),
    path('militares/<int:pk>/', views.MilitarDetailView.as_view(), name='militar-detail-view'),
    path('militares/<int:pk>/editar/', views.edit_militar, name='militar-edit_militar-view'),

    # Relatorios
    path('militares/<int:pk>/assentamentos/', views.gerate_assentamentos, name='militar-assentamentos-reportview'),
    path('escolaridade/relatorio/', views.escolaridade_report, name='militar-escolaridade-reportview'),
    path('religiao/relatorio/', views.religiao_report, name='militar-religiao-reportview'),
    path('geochart/relatorio/', views.geochart_report, name='militar-geochart-reportview'),

    # Mapa da Força
    path('militares/mapforce/list', views.map_force_list, name='militar-map_force_list-view'),
    path('militares/mapforce/tree', views.map_force_tree, name='militar-map_force_tree-view'),
    path('militares/mapforce/kaban', views.map_force_kaban, name='militar-map_force_kaban-view'),
    path('militares/mapforce/maps', views.map_force_maps, name='militar-map_force_maps-view'),
    path('militares/mapforce/diagram', views.map_force_diagram, name='militar-map_force_diagram-view'),

    # Jsons
    path('militares/pelotoes/json', views.get_pelotao_json, name='militar-get_pelotao-json'),
    path('militares/gcs/json', views.get_gc_json, name='militar-get_gc-json'),
]