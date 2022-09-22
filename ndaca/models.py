from django.db import models

# Create your models here.

#
# Categoria Conteudos atitudinais
#
class CategoriaConteudoAtitudinal(models.Model):
    nome      = models.CharField(max_length=250)
    class Meta:
        verbose_name = "Categoria de Conteúdo Atitudinal"
        verbose_name_plural = "Categorias de Conteúdo Atitudinal"

    def __str__(self):
        return self.nome or ""

#
# Conteudos atitudinais
#
class ConteudoAtitudinal(models.Model):
    nome      = models.CharField(max_length=250)
    categoria = models.ForeignKey(CategoriaConteudoAtitudinal, on_delete=models.CASCADE)
    detalhes  = models.TextField(blank=True, null=True)
    exemplos  = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "Conteúdo Atitudinal"
        verbose_name_plural = "Conteúdos Atitudinais"

    def __str__(self):
        return self.nome or ""