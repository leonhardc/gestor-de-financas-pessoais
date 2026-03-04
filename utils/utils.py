from financeiro.models import Transacao
from datetime import datetime


def filtrar_transacoes(transacoes, tipo=None, categoria=None, data_inicio=None, data_fim=None):
    filtros = {}
    
    if tipo is not None and tipo != '':
        filtros['tipo'] = tipo
    if categoria is not None and categoria != '':
        filtros['categoria__id'] = categoria
    if data_inicio is not None and data_inicio != '':
        filtros['data__gte'] = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    if data_fim is not None and data_fim != '':
        filtros['data__lte'] = datetime.strptime(data_fim, '%Y-%m-%d').date()
    if not filtros:
        return transacoes
    else:
        return transacoes.filter(**filtros)