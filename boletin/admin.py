from django.contrib import admin

# Register your models here.
from .models import TipoBoletin, BoletinDocumento

class BoletinDocumentoAdmin(admin.ModelAdmin):
	list_display = ("nome", "data_inicio", "data_final", "tipo")
	list_filter = ('tipo', )

admin.site.register(TipoBoletin)
admin.site.register(BoletinDocumento, BoletinDocumentoAdmin)