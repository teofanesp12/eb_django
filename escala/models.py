from django.db import models

# Create your models here.
from militares.models import Graduacao, Militar
from militares.models import SubUnidade, Pelotao

class MaterialAlterado(models.Model):
    ocorrencia  = models.CharField(max_length=250, verbose_name="Ocorrências")
    local = models.CharField(max_length=250)
    tipo  = models.CharField(max_length=50, verbose_name="Tipo", choices=[("danificado","Danificado"),("faltando","Faltando"),("queimado","Queimado") ], default="danificado")
    def __str__(self):
        return self.ocorrencia or ""

class InstalacaoAlterado(models.Model):
    ocorrencia  = models.CharField(max_length=250, verbose_name="Ocorrências")
    local = models.CharField(max_length=250)
    tipo  = models.CharField(max_length=50, verbose_name="Tipo", choices=[("danificado","Danificado"),("faltando","Faltando") ], default="danificado")
    def __str__(self):
        return self.ocorrencia or ""

def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = filename.split('.')
    if len(filename)>1:
        return 'ServicoLocal/{0}/{1}'.format(instance.pk, '{0}.{1}'.format(instance.nome,filename[1]))
    else:
        return 'ServicoLocal/{0}/{1}'.format(instance.pk, '{0}.{1}'.format(instance.nome,".file"))
class ServicoLocal(models.Model):
    nome      = models.CharField(max_length=250, verbose_name="Nome")
    latitude  = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True, verbose_name="Longitude")
    ativo     = models.BooleanField(default=True, verbose_name="Ativo?")
    subunidade = models.ForeignKey(SubUnidade, on_delete=models.SET_NULL, null=True, blank=True)
    pelotao    = models.ForeignKey(Pelotao, on_delete=models.SET_NULL, null=True, blank=True)

    arquivo_documentos  = models.FileField(upload_to=file_directory_path, null=True, blank=True)
    arquivo_fichas      = models.FileField(upload_to=file_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = "Local do Serviço"
        verbose_name_plural = "Locais do Serviço"

class Livro(models.Model):
    data        = models.DateField()
    local       = models.ForeignKey(ServicoLocal, on_delete=models.CASCADE, null=True)# No Null
    parada      = models.TextField(blank=True, null=True, verbose_name="Parada Diaria")
    ocorrencia  = models.TextField(blank=True, null=True, verbose_name="Ocorrências")
    material    = models.ManyToManyField(MaterialAlterado)
    instalacao  = models.ManyToManyField(InstalacaoAlterado)
    def __str__(self):
        return self.data or ""

class ServicoLocalLinha(models.Model):
    local      = models.ForeignKey(ServicoLocal, on_delete=models.CASCADE, null=True)# No Null
    graduacao  = models.ForeignKey(Graduacao, on_delete=models.CASCADE, verbose_name="Graduação")
    quantidade = models.IntegerField()# Quantidade de militares para a função.
    funcao     = models.CharField(max_length=250, verbose_name="Função no Serviço")
    livro      = models.BooleanField(default=False, verbose_name="Responsavel do Livro?")

    class Meta:
        verbose_name = "Local do Serviço Linha"
        verbose_name_plural = "Local do Serviço Linhas"

class ServicoEscala(models.Model):
    data    = models.DateField()
    locais  = models.ManyToManyField(ServicoLocal)
    livros  = models.ManyToManyField(Livro, blank=True)
    status  = models.CharField(max_length=50, verbose_name="Status", choices=[("rascunho","Rascunho"),("gerado","Gerado"),("publicado","Publicado"),("finalizado","Finalizado") ], default="rascunho")

    class Meta:
        verbose_name = "Escala de Serviço"
        verbose_name_plural = "Escalas de Serviço"
        ordering = ['data']

class ServicoEscalaLinha(models.Model):
    escala  = models.ForeignKey(ServicoEscala, on_delete=models.CASCADE)
    militar = models.ForeignKey(Militar, on_delete=models.CASCADE)
    militar_substituto  = models.ForeignKey(Militar, related_name="militar_substituto_pk", on_delete=models.SET_NULL, null=True, blank=True)
    data    = models.DateField()
    status  = models.CharField(max_length=50, verbose_name="Status", choices=[("rascunho","Rascunho"),("publicado","Publicado") ], default="rascunho")
    folga   = models.IntegerField(default=0)

class ServicoLocalLinhaDraft(models.Model):
    escala  = models.ForeignKey(ServicoEscala, on_delete=models.CASCADE)
    local_linha  = models.ForeignKey(ServicoLocalLinha, on_delete=models.CASCADE)
    # ServicoLocalLinha Filho
    graduacao  = models.ForeignKey(Graduacao, on_delete=models.CASCADE, verbose_name="Graduação")
    quantidade = models.IntegerField()# Quantidade de militares para a função.
    funcao     = models.CharField(max_length=250, verbose_name="Função no Serviço")
    livro      = models.BooleanField(default=False, verbose_name="Responsavel do Livro?")
    militar_escalado  = models.ForeignKey(Militar, on_delete=models.SET_NULL, null=True, blank=True)

    def restaurar(self):
        pass