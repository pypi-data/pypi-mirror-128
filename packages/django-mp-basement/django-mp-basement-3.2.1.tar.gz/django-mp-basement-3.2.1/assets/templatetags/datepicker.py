
from django import template


register = template.Library()


@register.inclusion_tag('datepicker.html', takes_context=True)
def datepicker_js(context):
    return context
