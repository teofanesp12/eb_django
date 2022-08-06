from django.db import models
from django.urls import reverse

# Create your models here.

class TipoTurma(models.Model):
    nome = models.CharField(max_length=250)
    codigo = models.CharField(max_length=150)
    descricao = models.TextField(null=True)
    capa = models.ImageField(upload_to = 'turma/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

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