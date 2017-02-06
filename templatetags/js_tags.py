from django import template
register = template.Library()

@register.filter
def chart_date(date):
    return "new Date({0}, {1}, {2}, {3}, {4})".format(date.year, date.month, date.day, date.hour, date.minute)