from django.db import models

# Create your models here.

class Banco(models.Model):
    nome   = models.CharField(max_length=250)
    codigo = models.CharField(max_length=4)

    def __str__(self):
        return self.nome or ""

class Religiao(models.Model):
    nome = models.CharField(max_length=250)
    class Meta:
        verbose_name = "Religião"
        verbose_name_plural = "Religiões"

    def __str__(self):
        return self.nome or ""

class Escolaridade(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self):
        return self.nome or ""


class Pais(models.Model):
    nome = models.CharField(max_length=250)
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Paises"

    def __str__(self):
        return self.nome or ""

class Estado(models.Model):
    uf   = models.CharField(max_length=2)
    nome = models.CharField(max_length=250)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return (self.uf or "") + " - " + (self.nome or "")

class Cidade(models.Model):
    nome   = models.CharField(max_length=250)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    latitude  = models.DecimalField(max_digits = 5, decimal_places = 2, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 5, decimal_places = 2, null=True, blank=True)

    def __str__(self):
        return self.nome or ""