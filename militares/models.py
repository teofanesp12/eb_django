from django.db import models
from django.urls import reverse
# Create your models here.

from base.models import Religiao, Escolaridade, Pais, Estado, Cidade, Banco

#
# Graduações militares
#

class Graduacao(models.Model):
    nome = models.CharField(max_length=250)
    abr  = models.CharField(max_length=150, null=True, verbose_name="Abreviãção")
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

class SubUnidade(models.Model):
    nome = models.CharField(max_length=250)
    abr = models.CharField(max_length=50, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    nome_historico = models.CharField(max_length=250, null=True, blank=True)
    unidade     = models.ForeignKey(Unidade, on_delete=models.SET_NULL, blank=True, null=True)
    logo = models.ImageField(upload_to = 'subunidades/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

class Pelotao(models.Model):
    nome = models.CharField(max_length=250)
    abr  = models.CharField(max_length=50, null=True, blank=True)
    ref  = models.CharField(max_length=250, null=True, blank=True)
    subunidade     = models.ForeignKey(SubUnidade, on_delete=models.SET_NULL, blank=True, null=True)
    logo = models.ImageField(upload_to = 'pelotoes/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

class GrupoCombate(models.Model):
    nome = models.CharField(max_length=250)
    abr  = models.CharField(max_length=50, null=True, blank=True)
    ref  = models.CharField(max_length=250, null=True, blank=True)
    pelotao     = models.ForeignKey(Pelotao, on_delete=models.SET_NULL, blank=True, null=True)
    logo = models.ImageField(upload_to = 'gruposcombates/', null=True, blank=True)

    def __str__(self):
        return self.nome or ""

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'militares/{0}/photo_{1}'.format(instance.numero, filename)

class Militar(models.Model):
    nome        = models.CharField(max_length=250, verbose_name="Nome Completo")
    nome_guerra = models.CharField(max_length=250)
    numero      = models.IntegerField(null=True, blank=True)
    identidade  = models.CharField(max_length=25, null=True, blank=True, unique=True, help_text="Identidade Militar")
    cpf         = models.CharField(max_length=25, null=True, blank=True, unique=True, verbose_name="CPF")
    rg          = models.CharField(max_length=25, null=True, blank=True, unique=True, verbose_name="RG")
    ra          = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="Registro de Alistamento")
    graduacao = models.ForeignKey(Graduacao, on_delete=models.CASCADE, verbose_name="Graduação")
    qm = models.ForeignKey(QualificacaoMilitar, on_delete=models.CASCADE, verbose_name="Qualificação Militar")
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.CASCADE)
    religiao     = models.ForeignKey(Religiao, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Religião")
    tipagem      = models.CharField(max_length=250, verbose_name="Tipagem Sanguinea/Fator RH")
    nascimento   = models.DateField(null=True, blank=True)
    naturalidade = models.ForeignKey(Cidade, related_name="natural", on_delete=models.SET_NULL, blank=True, null=True)
    pai = models.CharField(max_length=250, blank=True, null=True)
    mae = models.CharField(max_length=250, blank=True, null=True, verbose_name="Mãe")
    logradouro = models.CharField(max_length=250, blank=True, null=True)
    numero_endereco = models.CharField(max_length=250, blank=True, null=True, verbose_name="Número")
    bairro_endereco = models.CharField(max_length=250, blank=True, null=True, verbose_name="Bairro")
    complemento_endereco = models.CharField(max_length=250, blank=True, null=True, verbose_name="Complemento")
    cep_endereco = models.CharField(max_length=250, blank=True, null=True, verbose_name="CEP")
    cidade_endereco = models.ForeignKey(Cidade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Cidade")
    celular  = models.CharField(max_length=250, blank=True, null=True)
    telefone = models.CharField(max_length=250, blank=True, null=True)
    email    = models.EmailField(max_length=250, blank=True, null=True, verbose_name="E-mail")
    preccp   = models.CharField(max_length=25, null=True, blank=True, verbose_name="PrecCP")
    banco    = models.ForeignKey(Banco, on_delete=models.SET_NULL, blank=True, null=True)
    agencia  = models.CharField(max_length=11, null=True, blank=True)
    conta    = models.CharField(max_length=11, null=True, blank=True)
    conta_tipo = models.CharField(max_length=50, verbose_name="Tipo de Conta", choices=[("corrente","Corrente"), ("poupança","Poupança"), ("salario","Salario"), ("investimento","Investimento")], default="corrente")
    aptidao  = models.CharField(max_length=250, blank=True, null=True, help_text='Se o militar tem alguma aptidão, ou função')

    subunidade  = models.ForeignKey(SubUnidade, on_delete=models.SET_NULL, blank=True, null=True)
    pelotao     = models.ForeignKey(Pelotao, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Pelotão")
    grupo_combate     = models.ForeignKey(GrupoCombate, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grupo de Combate")
    funcao      = models.CharField(max_length=250, verbose_name="Função", blank=True, null=True, help_text='Cmt Cia, Cmt Pel, Adj Pel, Cmt GC, Cmt Esq, E1, A1?')
    photo = models.ImageField(upload_to = user_directory_path, null=True, blank=True)
    chave      = models.CharField(max_length=250, null=True)

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
    tipo     = models.CharField(max_length=5, choices=[("fo+","Positivo"), ("fo-","Negativo"), ("fo","Neutro")], default="fo")
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