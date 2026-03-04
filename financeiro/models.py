from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import Sum
import uuid
from datetime import datetime

# Class Conta representa uma conta financeira do usuário, como conta corrente, poupança, carteira, etc.
class Conta(models.Model):
    class TipoConta(models.TextChoices):
        CORRENTE = 'corrente', 'Conta Corrente'
        POUPANCA = 'poupança', 'Poupança'
        CARTEIRA = 'carteira', 'Carteira'
        INVESTIMENTO = 'investimento', 'Investimento'
        OUTROS = 'outros', 'Outros'
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, verbose_name='ID')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    tipo = models.CharField(max_length=20, choices=TipoConta.choices, verbose_name='Tipo da Conta')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Saldo Inicial')
    
    @property
    def saldo_atual(self):
        receitas = self.transacao_set.filter(tipo=Transacao.TipoTransacao.RECEITA).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        despesas = self.transacao_set.filter(tipo=Transacao.TipoTransacao.DESPESA).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        return self.saldo_inicial + receitas - despesas

    def __str__(self):
        return f"{self.nome} ({self.usuario.username})"

# Class Categoria representa uma categoria para classificar as transações, como alimentação, transporte, lazer, etc. 
# Cada categoria é associada a um usuário e tem um tipo (receita ou despesa).
class Categoria(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, verbose_name='ID')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    nome = models.CharField(max_length=100, verbose_name='Nome da Categoria')
    tipo = models.CharField(
        max_length=20,
        choices=(('receita', 'Receita'), ('despesa', 'Despesa')),
        verbose_name='Tipo da Categoria'
    )
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    
    @property
    def despesa_categoria(self):
        if self.tipo == 'despesa':
            return self.transacao_set.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        return Decimal('0.00')
    
    @property
    def receita_categoria(self):
        if self.tipo == 'receita':
            return self.transacao_set.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        return Decimal('0.00')
    
    class Meta:
        unique_together = ('usuario', 'nome', 'tipo')
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

# Class Transacao representa uma transação financeira, que pode ser uma receita ou despesa, associada a 
# uma conta específica do usuário.
class Transacao(models.Model):
    class TipoTransacao(models.TextChoices):
        RECEITA = 'receita', 'Receita'
        DESPESA = 'despesa', 'Despesa'
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, verbose_name='ID')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name='Conta')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name='Categoria')
    tipo = models.CharField(max_length=20, choices=TipoTransacao.choices, verbose_name='Tipo da Transação')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data = models.DateField(verbose_name='Data')
    paga = models.BooleanField(default=True, verbose_name='Paga')
    descricao = models.CharField(max_length=255, blank=True, verbose_name='Descrição')
    parcela_numero = models.PositiveIntegerField(null=True, blank=True, verbose_name='Número da Parcela')
    total_parcelas = models.PositiveIntegerField(null=True, blank=True, verbose_name='Total de Parcelas')
    recorrente = models.BooleanField(default=False, verbose_name='Recorrente')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    atualizada_em = models.DateTimeField(auto_now=True, verbose_name='Atualizada em')

    class Meta:
        ordering = ['-data', '-criada_em']
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['data']),
            models.Index(fields=['conta']),
        ]

    def __str__(self):        
        return f"{self.tipo.capitalize()} de R${self.valor} em {self.data} - {self.conta.nome}"

# OrcamentoMensal representa o orçamento mensal do usuário para um determinado mês e ano, associado a uma conta específica. 
# Ele inclui o valor orçado e o valor gasto para aquele período.
class OrcamentoMensal(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, verbose_name='ID')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Conta')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoria')
    ano = models.PositiveIntegerField(default=datetime.now().year, verbose_name='Ano')
    mes = models.PositiveIntegerField(default=datetime.now().month, verbose_name='Mês')
    valor_orcado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor Orçado')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    @property
    def valor_gasto(self):
        transacoes = Transacao.objects.filter(usuario=self.usuario, tipo='despesa', categoria=self.categoria, data__year=self.ano, data__month=self.mes)
        return transacoes.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    
    @property
    def percentual(self):
        if self.valor_orcado == 0:
            return 0
        return (self.valor_gasto / self.valor_orcado) * 100
    
    class Meta:
        # unique_together = ("usuario", "conta", "categoria", "ano", "mes")
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'conta', 'categoria', 'ano', 'mes'], name='unique_orcamento_mensal')
        ]   
        ordering = ['-ano', '-mes']

# SnapshotMensal representa um resumo mensal das finanças do usuário, incluindo o saldo final,
# total de receitas e despesas para um determinado mês e ano. Ele é associado a um usuário e 
# opcionalmente a uma conta específica.
class SnapshotMensal(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, verbose_name='ID')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    conta = models.ForeignKey("Conta", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Conta')
    ano = models.PositiveIntegerField(default=datetime.now().year, verbose_name='Ano')
    mes = models.PositiveIntegerField(default=datetime.now().month, verbose_name='Mês')
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Saldo Final')
    total_receitas = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total de Receitas')
    total_despesas = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total de Despesas')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        unique_together = ("usuario", "conta", "ano", "mes")
        ordering = ['-ano', '-mes']


