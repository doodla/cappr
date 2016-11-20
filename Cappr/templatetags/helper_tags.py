from django import template

register = template.Library()


@register.filter
def cost_to_usd(value):
    return "{0:.2f}".format(value / 100)
