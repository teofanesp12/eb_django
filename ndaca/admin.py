from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import CategoriaConteudoAtitudinal, ConteudoAtitudinal

class CategoriaConteudoAtitudinalAdmin(ImportExportModelAdmin):
    # list_filter = ('materia', )
    search_fields = ['nome']

class ConteudoAtitudinalAdmin(ImportExportModelAdmin):
    list_filter = ('categoria', )
    search_fields = ['nome']

admin.site.register(ConteudoAtitudinal, ConteudoAtitudinalAdmin)
admin.site.register(CategoriaConteudoAtitudinal, CategoriaConteudoAtitudinalAdmin)