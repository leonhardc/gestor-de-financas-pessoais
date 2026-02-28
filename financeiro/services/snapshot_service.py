from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

def gerar_snapshot(usuario, conta, ano, mes):
    from financeiro.models import Transacao, SnapshotMensal

    receitas = Transacao.objects.filter(
        usuario=usuario,
        conta=conta,
        tipo="receita",
        data__year=ano,
        data__month=mes
    ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

    despesas = Transacao.objects.filter(
        usuario=usuario,
        conta=conta,
        tipo="despesa",
        data__year=ano,
        data__month=mes
    ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

    saldo_final = conta.saldo_inicial + receitas - despesas

    SnapshotMensal.objects.update_or_create(
        usuario=usuario,
        conta=conta,
        ano=ano,
        mes=mes,
        defaults={
            "saldo_final": saldo_final,
            "total_receitas": receitas,
            "total_despesas": despesas,
        }
    )