# usuarios/templatetags/calendar_extras.py

from django import template
import calendar

register = template.Library()

@register.filter
def to_range(value):
    """
    Cria um range de 1 até o valor especificado (inclusive).
    Uso no template: {% for month in 12|to_range %}
    """
    return range(1, value + 1)

@register.filter
def month_name(month_number):
    """
    Converte um número de mês para seu nome em português.
    Exemplo: 1 -> Janeiro
    """
    return calendar.month_name[month_number]

@register.filter
def get_calendar(month, year):
    """
    Retorna a estrutura do calendário para um determinado mês e ano.
    """
    cal = calendar.Calendar(firstweekday=6)  # Domingo como primeiro dia da semana
    return cal.monthdayscalendar(year, month)
