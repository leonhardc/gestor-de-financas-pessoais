from django.contrib import admin
from .models import Conta, Transacao, Categoria, OrcamentoMensal


class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario', 'ativa', 'criada_em')
    list_filter = ('tipo', 'ativa')
    search_fields = ('nome', 'usuario__username')
    ordering = ('-criada_em',)
    class Meta:
        model = Conta
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'


class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'valor', 'data', 'conta', 'usuario', 'paga')
    list_filter = ('tipo', 'paga', 'data')
    search_fields = ('descricao', 'conta__nome', 'usuario__username')
    ordering = ('-data', '-criada_em')
    class Meta:
        model = Transacao
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario', 'criada_em')
    list_filter = ('tipo',)
    search_fields = ('nome', 'usuario__username')
    ordering = ('nome',)
    class Meta:
        model = Categoria
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class OrcamentoMensalAdmin(admin.ModelAdmin):
    list_display = ('conta', 'categoria', 'ano', 'mes', 'valor_orcado', 'valor_gasto')
    list_filter = ('ano', 'mes')
    search_fields = ('conta__nome', 'categoria__nome', 'usuario__username')
    ordering = ('-ano', '-mes')
    class Meta:
        model = OrcamentoMensal
        verbose_name = 'Orçamento Mensal'
        verbose_name_plural = 'Orçamentos Mensais'

admin.site.register(Conta, ContaAdmin)
admin.site.register(Transacao, TransacaoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(OrcamentoMensal, OrcamentoMensalAdmin)
