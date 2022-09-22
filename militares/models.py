from django.db import models
from django.urls import reverse
# Create your models here.

from base.models import Religiao, Escolaridade, Pais, Estado, Cidade

#
# Graduações militares
#

class Graduacao(models.Model):
    nome = models.CharField(max_length=250)
    class Meta:
        verbose_name = "Graduação"
        verbose_name_plural = "Graduações"

    def __str__(self):
        return self.nome or ""
#
# Infantaria, etc
#
class QualificacaoMilitar(models.Model):
    nome = models.CharField(max_length=250)
    class Meta:
        verbose_name = "Qualificação Militar"
        verbose_name_plural = "Qualificações Militares"

    def __str__(self):
        return self.nome or ""

class Unidade(models.Model):
    nome = models.CharField(max_length=250)
    abr = models.CharField(max_length=50)
    ref = models.CharField(max_length=250)
    nome_historico = models.CharField(max_length=250)
    logo = models.ImageField(upload_to = 'unidades/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'militar_{0}/{1}'.format(instance.numero, filename)

class Militar(models.Model):
    nome        = models.CharField(max_length=250)
    nome_guerra = models.CharField(max_length=250)
    numero      = models.IntegerField(null=True, blank=True)
    identidade  = models.CharField(max_length=25, null=True, blank=True)
    preccp      = models.CharField(max_length=25, null=True, blank=True)
    ra          = models.CharField(max_length=30, null=True, blank=True)
    graduacao = models.ForeignKey(Graduacao, on_delete=models.CASCADE)
    qm = models.ForeignKey(QualificacaoMilitar, on_delete=models.CASCADE)
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.CASCADE)
    religiao     = models.ForeignKey(Religiao, on_delete=models.SET_NULL, blank=True, null=True)
    tipagem      = models.CharField(max_length=250)
    naturalidade = models.ForeignKey(Cidade, related_name="natural", on_delete=models.SET_NULL, blank=True, null=True)
    pai = models.CharField(max_length=250, blank=True, null=True)
    mae = models.CharField(max_length=250, blank=True, null=True)
    logradouro = models.CharField(max_length=250, blank=True, null=True)
    numero_endereco = models.CharField(max_length=250, blank=True, null=True)
    bairro_endereco = models.CharField(max_length=250, blank=True, null=True)
    complemento_endereco = models.CharField(max_length=250, blank=True, null=True)
    cep_endereco = models.CharField(max_length=250, blank=True, null=True)
    cidade_endereco = models.ForeignKey(Cidade, on_delete=models.SET_NULL, blank=True, null=True)
    celular  = models.CharField(max_length=250, blank=True, null=True)
    telefone = models.CharField(max_length=250, blank=True, null=True)
    email    = models.EmailField(max_length=250, blank=True, null=True)
    aptidao  = models.CharField(max_length=250, blank=True, null=True, help_text='Se o militar tem alguma aptidão, ou função')

    photo = models.ImageField(upload_to = user_directory_path, null=True, blank=True)

    # visitas_medicas = models.ManyToManyField(VisitaMedica)

    class Meta:
        ordering = ['numero','nome']
        verbose_name_plural = "Militares"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        # print(reverse('militar-detail-view', current_app="militar", kwargs={'militar_id' : self.pk}))
        a = reverse('militar:militar-detail-view', kwargs={'pk' : self.pk})
        return a
    def __str__(self):
        return self.nome or ""

#
# Visita medica
#
class VisitaMedica(models.Model):
    motivo   = models.CharField(max_length=250)
    detalhes = models.TextField(blank=True, null=True)
    data     = models.DateField(blank=True, null=True)

    militar = models.ForeignKey(Militar, on_delete=models.CASCADE, null=True)
    medico     = models.CharField(max_length=250, blank=True, null=True)

    dipensado_formatura = models.BooleanField()
    dipensado_uniforme = models.BooleanField()
    dipensado_campo = models.BooleanField()
    dipensado_tfm = models.BooleanField()
    dispensado_detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.motivo or ""
from ndaca.models import ConteudoAtitudinal
#
# gerar punição a partir do FO
#
class FatoObservado(models.Model):
    militar  = models.ForeignKey(Militar, on_delete=models.CASCADE, null=True)
    motivo   = models.CharField(max_length=250)
    conteudo_atitudinal = models.ForeignKey(ConteudoAtitudinal, on_delete=models.SET_NULL, null=True)
    tipo     = models.CharField(max_length=250, choices=[("fo+","Positivo"), ("fo-","Negativo"), ("fo","Neutro")], default="fo")
    detalhes = models.TextField(blank=True, null=True)
    data     = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.motivo or ""
#
# Punições
#
class Punicao(models.Model):
    militar  = models.ForeignKey(Militar, on_delete=models.CASCADE, null=True)
    motivo   = models.CharField(max_length=250)
    detalhes = models.TextField(blank=True, null=True)
    data     = models.DateField(blank=True, null=True)
    tipo     = models.CharField(max_length=250, blank=True, null=True)
    bi       = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Punição"
        verbose_name_plural = "Punições"

    def __str__(self):
        return self.motivo or ""
#
# Elogios
#
class Elogio(models.Model):
    militar  = models.ForeignKey(Militar, on_delete=models.CASCADE, null=True)
    motivo   = models.CharField(max_length=250)
    detalhes = models.TextField(blank=True, null=True)
    data     = models.DateField(blank=True, null=True)
    tipo     = models.CharField(max_length=250, blank=True, null=True)
    bi       = models.CharField(max_length=250)

    def __str__(self):
        return self.motivo or ""