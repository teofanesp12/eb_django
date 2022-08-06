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

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'pp'

urlpatterns = [
    path('', views.home, name='home'),
    path('turmapp/<int:turma_id>/', views.turma, name='turma'),
    path('materia/<int:materia_id>/', views.materia, name='materia'),
    path('objetivo/<int:objetivo_id>/', views.objetivo, name='objetivo'),
    path('objetivo/<int:objetivo_id>/gerar_plano_session', views.gerar_plano_session, name='gerar_plano_session'),
]