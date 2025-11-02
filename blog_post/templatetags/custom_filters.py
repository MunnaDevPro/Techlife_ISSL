
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def humanize_number(value):

    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value >= 1_000_000:
     
        return f"{value / 1_000_000:.1f}M"
    elif value >= 10_000:
       
        return f"{value / 1000:.0f}k"
    elif value >= 1_000:
      
        return f"{value / 1000:.1f}k"
    else:
      
        return value