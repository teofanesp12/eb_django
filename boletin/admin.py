from django.contrib import admin

# Register your models here.
from .models import TipoBoletin, BoletinDocumento
admin.site.register(TipoBoletin)
admin.site.register(BoletinDocumento)