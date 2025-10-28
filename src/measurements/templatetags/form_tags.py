from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    """Adiciona classes CSS ao campo"""
    return field.as_widget(attrs={"class": css})

@register.filter
def add_error_class(field, bound_field):
    """Adiciona classe 'is-invalid' se o campo tem erro"""
    if bound_field.errors:
        return field.as_widget(attrs={"class": field.field.widget.attrs.get("class", "") + " is-invalid"})
    return field
