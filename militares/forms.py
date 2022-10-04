from django import forms

from .models import FatoObservado

"""
from datetime import date
class FOForm(forms.Form):
	motivo = forms.CharField(max_length=250)
	detalhes = forms.CharField(widget=forms.Textarea)
	data = forms.DateField(initial=date.today)
"""
class FatoObservadoForm(forms.ModelForm):
    class Meta:
        model = FatoObservado
        fields = ['motivo', 'conteudo_atitudinal', 'tipo', 'detalhes', 'data']
        # widgets = {'data': forms.DateField(initial=date.today)}