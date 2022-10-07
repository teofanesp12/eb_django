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
    path('militares/<int:pk>/assentamentos/', views.gerate_assentamentos, name='militar-assentamentos-reportview'),
    path('escolaridade/relatorio/', views.escolaridade_report, name='militar-escolaridade-reportview'),
    path('religiao/relatorio/', views.religiao_report, name='militar-religiao-reportview'),
    path('geochart/relatorio/', views.geochart_report, name='militar-geochart-reportview'),
]