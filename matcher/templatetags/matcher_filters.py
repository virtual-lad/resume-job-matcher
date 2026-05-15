from django import template

register = template.Library()


@register.filter(name="trim")
def trim(value):
    """Strip leading/trailing whitespace from a string."""
    return str(value).strip()
