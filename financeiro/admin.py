from django.contrib import admin
from .models import Conta


class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario', 'ativa', 'criada_em')
    list_filter = ('tipo', 'ativa')
    search_fields = ('nome', 'usuario__username')
    ordering = ('-criada_em',)
    class Meta:
        model = Conta
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

admin.site.register(Conta, ContaAdmin)
