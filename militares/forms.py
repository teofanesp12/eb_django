from django import forms

from .models import FatoObservado, Militar

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

class MilitarForm(forms.ModelForm):
    class Meta:
        model = Militar
        fields = '__all__'
        # fields = ['name', 'title', 'birth_date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            field = self.fields[f]
            if f in ['celular_is_whatsapp']:
                field.widget.attrs.update({'class': 'form-check-input'})
            elif f in ['graduacao','qm', 'escolaridade', 'religiao', 'naturalidade', 'cidade_endereco', 'cidade_endereco', 'banco', 'subunidade', 'pelotao', 'grupo_combate','conta_tipo', 'cnh_categoria']:
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})