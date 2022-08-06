from django.contrib import admin

# Register your models here.

from .models import Materia, Objetivo, ObjetivoParcial, Assunto, SubAssunto, FileDoc

from .models import TipoTurma

class ObjetivoAdminInline(admin.StackedInline):
    model = Objetivo
    extra = 0
class MateriaAdmin(admin.ModelAdmin):
    inlines = (ObjetivoAdminInline, )
    # autocomplete_fields = ['tipo_turma']

class AssuntoAdminInline(admin.StackedInline):
    model = Assunto
    extra = 0
class SubAssuntoAdminInline(admin.StackedInline):
    model = SubAssunto
    extra = 0
class AssuntoAdmin(admin.ModelAdmin):
    inlines = (SubAssuntoAdminInline, )
    autocomplete_fields = ['objetivo']
    search_fields = ['nome']
class SubAssuntoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['assunto']

class FileDocAdminInline(admin.StackedInline):
    model = FileDoc
    extra = 0
class ObjetivoAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'codigo']
    inlines = (AssuntoAdminInline, FileDocAdminInline, )

class ObjetivoParcialAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'codigo']
    filter_horizontal = ('objetivos',)

admin.site.register(TipoTurma)
admin.site.register(FileDoc)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Objetivo, ObjetivoAdmin)
admin.site.register(ObjetivoParcial, ObjetivoParcialAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(SubAssunto, SubAssuntoAdmin)