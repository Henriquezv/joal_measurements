from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.contrib.auth.models import Group


class MeasurementsGroup(Group):
    class Meta:
        proxy = True
        verbose_name = "Measurement Group"
        verbose_name_plural = "Measurement Groups"

class CompanyRole(models.TextChoices):
    AUXILIAR_ENGENHARIA = "AuxiliarEngenharia", "Auxiliar de Engenharia"
    ENGENHEIRO = "Engenheiro", "Engenheiro"
    GERENTE = "Gerente", "Gerente"
    DIRETOR = "Diretor", "Diretor"


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("O campo login é obrigatório")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)

    # flags necessárias pro admin do Django
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    company_role = models.CharField(
        max_length=50,
        choices=CompanyRole.choices,
        blank=True,
        null=True
    )
    company_id = models.IntegerField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
