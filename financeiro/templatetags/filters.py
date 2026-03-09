from django import template
import calendar
import locale

register = template.Library()
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

@register.filter
def mes_por_extensso(numero_mes):
    try:
        if 1<= numero_mes <= 12:
            return str.capitalize(calendar.month_name[numero_mes])
        else:
            return "Mês inválido"
    except (ValueError, TypeError):
        return "Entrada inválida"