from django.db import models

# Create your models here.

class CompanyRole(models.TextChoices):
    AUXILIAR_ENGENHARIA = "AuxiliarEngenharia", "Auxiliar Engenharia"
    ENGENHEIRO = "Engenheiro", "Engenheiro"
    GERENTE = "Gerente", "Gerente"
    DIRETOR = "Diretor", "Diretor"

class BusinessInfo(models.Model):
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # armazenar hash
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    company_role = models.CharField(
        max_length=50,
        default=CompanyRole.ENGENHEIRO
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
