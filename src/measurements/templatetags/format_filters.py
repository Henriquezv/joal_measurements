from django import template

register = template.Library()

@register.filter
def money_format(value):
    """Formata número como moeda brasileira: 33.412,00"""
    try:
        value = float(value)
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value
