from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import Religiao, Escolaridade

admin.site.register(Religiao)
admin.site.register(Escolaridade)

from .models import Banco
admin.site.register(Banco)

from .models import Pais, Estado, Cidade
class EstadoAdminInline(admin.TabularInline):
    model = Estado
class PaisAdmin(admin.ModelAdmin):
    inlines = (EstadoAdminInline, )
class CidadeAdminInline(admin.TabularInline):
    model = Cidade


class CidadeAdmin(ImportExportModelAdmin):
    search_fields = ['nome']
class EstadoAdmin(ImportExportModelAdmin):
    inlines = (CidadeAdminInline, )
    search_fields = ['nome']


admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Estado, EstadoAdmin)
