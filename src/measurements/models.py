from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field



class MeasurementStatus(models.TextChoices):
    IN_PROGRESS = "InProgress", "Em andamento (Engenheiro)"
    PENDING_MANAGER = "PendingManagerApproval", "Pendente aprovação Gerente"
    PENDING_DIRECTOR = "PendingDirectorApproval", "Pendente aprovação Diretor"
    FINISHED = "Finished", "Liberado"


class Measurement(models.Model):
    name = models.CharField(max_length=255)
    contract = models.CharField(max_length=255, blank=True, null=True)  
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    description = CKEditor5Field('Descrição', config_name='default', blank=True, null=True)
    attachment = models.FileField(upload_to="measurements/files/", blank=True, null=True)

    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounts = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounts_detail = models.TextField(blank=True, null=True)
    final_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=MeasurementStatus.choices,
        default=MeasurementStatus.IN_PROGRESS
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="measurements")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MeasurementMessage(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: {self.message[:30]}"
