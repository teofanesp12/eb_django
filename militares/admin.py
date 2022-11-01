from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from .models import Militar
from .models import Graduacao, QualificacaoMilitar
from .models import Unidade, SubUnidade, Pelotao, GrupoCombate

admin.site.register(Unidade)
admin.site.register(SubUnidade)
admin.site.register(Pelotao)
admin.site.register(GrupoCombate)

admin.site.register(Graduacao)
admin.site.register(QualificacaoMilitar)


from .models import VisitaMedica
class VisitaMedicaAdminInline(admin.TabularInline):
    model = VisitaMedica
    extra = 0
class VisitaMedicaAdmin(admin.ModelAdmin):
    list_display = ("motivo", "data")
    save_on_top = True
    fieldsets = (
        ("Identificação", {
            'fields': ('militar',)
        }),
        ('Detalhes', {
            'fields': ('motivo', 'data', 'medico', 'detalhes')
        }),
        ('Dispensado?', {
            'classes': ('collapse','extrapretty'),
            'fields': ('dipensado_formatura', 'dipensado_uniforme', 'dipensado_campo', 'dipensado_tfm', 'dispensado_detalhes')
        }),
    )
admin.site.register(VisitaMedica, VisitaMedicaAdmin)

#
# Elogio e Punicao
#
from .models import Punicao, Elogio
class PunicaoAdminInline(admin.TabularInline):
    model = Punicao
    extra = 0
class ElogioAdminInline(admin.TabularInline):
    model = Elogio
    extra = 0
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ("motivo", "data", "bi")
admin.site.register(Punicao, PunicaoAdmin)
class ElogioAdmin(admin.ModelAdmin):
    list_display = ("motivo", "data", "bi")
admin.site.register(Elogio, ElogioAdmin)


from .models import FatoObservado
class FatoObservadoAdmin(admin.ModelAdmin):
    list_display = ("militar", "motivo", "tipo", "data")
    radio_fields = {"tipo": admin.VERTICAL}
class FatoObservadoAdminInline(admin.TabularInline):
    model = FatoObservado
    extra = 0
admin.site.register(FatoObservado, FatoObservadoAdmin)


class MilitarAdmin(ImportExportModelAdmin):
    list_display = ("graduacao", "numero", "nome")
    search_fields = ['nome']
    autocomplete_fields = ['naturalidade', 'cidade_endereco']
    save_on_top = True
    fieldsets = (
        ("Identificação", {
            'fields': ('nome', 'nome_guerra', 'numero', 'cpf', 'rg','identidade', 'ra', 'cnh', 'cnh_categoria', 'graduacao', 'qm', 'chave', 'photo')
        }),
        ('Detalhes', {
            'fields': ('aptidao', 'escolaridade', 'religiao', 'tipagem', 'naturalidade', 'nascimento', 'pai', 'mae')
        }),
        ('Endereço & Contato', {
            'fields': ('logradouro', 'numero_endereco', 'bairro_endereco', 'complemento_endereco', 'cep_endereco', 'cidade_endereco', 'endereco_latitude', 'endereco_longitude', 'celular', 'celular_is_whatsapp', 'telefone', 'email')
        }),
        ('Dados Bancários', {
            'fields': ('preccp', 'banco', 'agencia', 'conta', 'conta_tipo')
        }),
        ('Mapa da Força', {
            'fields': ('subunidade', 'pelotao', 'grupo_combate', 'funcao')
        }),
    )
    inlines = (VisitaMedicaAdminInline, PunicaoAdminInline, ElogioAdminInline, FatoObservadoAdminInline)
admin.site.register(Militar, MilitarAdmin)
