from django import forms

from .models import ServicoLocal, ServicoLocalLinha

class ServicoLocalForm(forms.ModelForm):
    class Meta:
        model = ServicoLocal
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            field = self.fields[f]
            if f in ['subunidade', 'pelotao']:
                field.widget.attrs.update({'class': 'form-select', "placeholder":field.label})
            elif f in ['detalhes']:
                field.widget.attrs.update({'class': 'form-control', "placeholder":field.label, "style":"height: 200px;"})
            else:
                field.widget.attrs.update({'class': 'form-control', "placeholder":field.label})

class ServicoLocalLinhaForm(forms.ModelForm):
    class Meta:
        model = ServicoLocalLinha
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.keys():
            field = self.fields[f]
            if f in ['livro']:
                field.widget.attrs.update({'class': 'form-check-input'})
            elif f in ['graduacao', 'local']:
                field.widget.attrs.update({'class': 'form-select', "placeholder":field.label})
            elif f in ['detalhes']:
                field.widget.attrs.update({'class': 'form-control', "placeholder":field.label, "style":"height: 200px;"})
            else:
                field.widget.attrs.update({'class': 'form-control', "placeholder":field.label})