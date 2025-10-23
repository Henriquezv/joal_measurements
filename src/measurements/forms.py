from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Measurement, MeasurementMessage


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "name",
            "contract",
            "payment_date",
            "value",
            "discounts",
            "discounts_detail",
            "final_value",
            "description",
            "attachment",
        ]
        labels = {
            "name": "Nome da Medição",
            "contract": "Contrato",
            "payment_date": "Data de Pagamento",
            "value": "Valor Bruto",
            "discounts": "Descontos",
            "discounts_detail": "Detalhes dos Descontos",
            "final_value": "Valor Final",
            "description": "Descrição",
            "attachment": "Anexo",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contract": forms.TextInput(attrs={"class": "form-control"}),
            "payment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "discounts": forms.NumberInput(attrs={"class": "form-control"}),
            "discounts_detail": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "final_value": forms.NumberInput(attrs={"class": "form-control"}),
            "description": CKEditor5Widget(config_name="default"),
        }

class MeasurementMessageForm(forms.ModelForm):
    class Meta:
        model = MeasurementMessage
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Digite uma mensagem...",
                "class": "form-control"
            }),
        }
        labels = {
            "message": "",
        }
