from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import Materia, Objetivo, ObjetivoParcial, Assunto, SubAssunto, FileDoc

from .models import TipoTurma

class ObjetivoAdminInline(admin.StackedInline):
    model = Objetivo
    extra = 0
class MateriaAdmin(ImportExportModelAdmin):
    inlines = (ObjetivoAdminInline, )
    # autocomplete_fields = ['tipo_turma']

class AssuntoAdminInline(admin.StackedInline):
    model = Assunto
    extra = 0
class SubAssuntoAdminInline(admin.StackedInline):
    model = SubAssunto
    extra = 0
class AssuntoAdmin(ImportExportModelAdmin):
    list_display = ("objetivo_codigo", "nome")
    inlines = (SubAssuntoAdminInline, )
    autocomplete_fields = ['objetivo']
    search_fields = ['nome']
    list_filter = ('objetivo__materia', )

    @admin.display(empty_value='???')
    def objetivo_codigo(self, obj):
        return obj.objetivo and obj.objetivo.codigo or ""
class SubAssuntoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['assunto']

class FileDocAdminInline(admin.StackedInline):
    model = FileDoc
    extra = 0
class ObjetivoAdmin(ImportExportModelAdmin):
    search_fields = ['nome', 'codigo']
    list_filter = ('materia', )
    list_display = ("codigo", "nome")
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