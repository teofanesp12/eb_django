from django.db import models
from django.urls import reverse

# Create your models here.

class TipoTurma(models.Model):
    nome = models.CharField(max_length=250)
    codigo = models.CharField(max_length=150)
    descricao = models.TextField(null=True)
    capa = models.ImageField(upload_to = 'turma/', null=True, blank=True)

    def __str__(self):
        return "%s - %s"%(self.nome or "", self.codigo or "")

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        # print(reverse('militar-detail-view', current_app="militar", kwargs={'militar_id' : self.pk}))
        return reverse('pp:turma', kwargs={'turma_id' : self.pk})

class Materia(models.Model):
    nome = models.CharField(max_length=200)
    tempo_diurno = models.IntegerField(default=0)
    tempo_noturno = models.IntegerField(default=0)
    tipo_turma = models.ForeignKey(TipoTurma, on_delete=models.CASCADE, null=True)# remove null
    capa = models.ImageField(upload_to = 'materia/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        # print(reverse('militar-detail-view', current_app="militar", kwargs={'militar_id' : self.pk}))
        return reverse('pp:materia', kwargs={'materia_id' : self.pk})

def capa_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'objetivo_{0}/{1}'.format(instance.pk, filename)
class Objetivo(models.Model):
    nome = models.CharField(max_length=500)
    codigo = models.CharField(max_length=100, null=True)# Remove null
    condicao = models.TextField(null=True)
    minimo = models.TextField(null=True)
    intermediario = models.TextField(null=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    capa = models.ImageField(upload_to = capa_directory_path, null=True, blank=True)

    def __str__(self):
        return self.nome or ""

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        # print(reverse('militar-detail-view', current_app="militar", kwargs={'militar_id' : self.pk}))
        return reverse('pp:objetivo', kwargs={'objetivo_id' : self.pk})

    class Meta:
        ordering = ['materia', 'codigo']

class ObjetivoParcial(models.Model):
    nome   = models.CharField(max_length=500)
    codigo = models.CharField(max_length=5)# Remove null
    info   = models.TextField(null=True)
    objetivos = models.ManyToManyField(Objetivo, blank=True)

    def __str__(self):
        return self.nome or ""

class Assunto(models.Model):
    nome = models.CharField(max_length=300)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome or ""

    class Meta:
        ordering = ['objetivo', ]
class SubAssunto(models.Model):
    nome = models.CharField(max_length=300)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome or ""

'''
 class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
 '''

class FatorRisco(models.Model):
    nome   = models.TextField()
    probabilidade = models.IntegerField()
    gravidade     = models.CharField(max_length=1)
    tipo          = models.CharField(max_length=50, choices=[("operacional","Operacional"), ("humano","Humano"), ("material","Material")], default='operacional')

    mitigadora    = models.TextField(null=True, blank=True)
    probabilidade_residual = models.IntegerField(null=True, blank=True)
    gravidade_residual     = models.CharField(max_length=1, null=True, blank=True)

    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nome or ""

    def _class_risco_all(self, residual=False):
        result=['Inaceitavel', 'Muito Alto', 'Alto', 'Medio', 'Baixo']
        if residual:
            probabilidade = self.probabilidade_residual
            gravidade = self.gravidade_residual
        else:
            probabilidade = self.probabilidade
            gravidade = self.gravidade
        if probabilidade == 5:
            if gravidade=='A':
                return result[0]# 'inaceitavel'
            elif gravidade in ['B','C']:
                return result[1]# 'muito_alto'
            elif gravidade=='D':
                return result[2]# 'alto'
            elif gravidade=='E':
                return result[3]# 'Medio'
        elif probabilidade == 4:
            if gravidade in ['A','B']:
                return result[1]
            elif gravidade in ['C']:
                return result[2]
            elif gravidade in ['D','E']:
                return result[3]
        elif probabilidade == 3:
            if gravidade in ['A']:
                return result[1]
            elif gravidade in ['B']:
                return result[2]
            elif gravidade in ['C']:
                return result[3]
            elif gravidade in ['D','E']:
                return result[4]
        elif probabilidade == 2:
            if gravidade in ['A']:
                return result[2]
            elif gravidade in ['B','C']:
                return result[3]
            elif gravidade in ['D','E']:
                return result[4]
        elif probabilidade == 1:
            return result[4]
        return '-'

    def class_risco(self):
        return self._class_risco_all()
    def class_risco_residual(self):
        return self._class_risco_all(residual=True)


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = filename.split('.')
    if len(filename)>1:
        return 'objetivo_{0}/{1}'.format(instance.objetivo.codigo, '{0}.{1}'.format(instance.nome,filename[1]))
    else:
        return 'objetivo_{0}/{1}'.format(instance.objetivo.codigo, '{0}.{1}'.format(instance.nome,".file"))

class FileDoc(models.Model):
    nome     = models.CharField(max_length=500)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, null=True)
    arquivo  = models.FileField(upload_to=file_directory_path)
    def __str__(self):
        return self.nome or ""