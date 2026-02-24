from django.db import models
from django.contrib.auth.models import User

# Class Conta representa uma conta financeira do usuário, como conta corrente, poupança, carteira, etc.
class Conta(models.Model):
    class TipoConta(models.TextChoices):
        CORRENTE = 'corrente', 'Conta Corrente'
        POUPANCA = 'poupança', 'Poupança'
        CARTEIRA = 'carteira', 'Carteira'
        INVESTIMENTO = 'investimento', 'Investimento'
        OUTROS = 'outros', 'Outros'
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    tipo = models.CharField(max_length=20, choices=TipoConta.choices, verbose_name='Tipo da Conta')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    def __str__(self):
        return f"{self.nome} ({self.usuario.username})"

# Class Transacao representa uma transação financeira, que pode ser uma receita ou despesa, associada a uma conta específica do usuário.
class Transacao(models.Model):
    class TipoTransacao(models.TextChoices):
        RECEITA = 'receita', 'Receita'
        DESPESA = 'despesa', 'Despesa'
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name='Conta')
    tipo = models.CharField(max_length=20, choices=TipoTransacao.choices, verbose_name='Tipo da Transação')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data = models.DateField(verbose_name='Data')
    descricao = models.CharField(max_length=255, blank=True, verbose_name='Descrição')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    
    def __str__(self):        
        return f"{self.tipo.capitalize()} de R${self.valor} em {self.data} - {self.conta.nome}"