from datetime import timezone
from django.shortcuts import render
from .models import Conta, Transacao, Categoria
from .forms import ContaForm, TransacaoForm, CategoriaForm


# CRUD de Conta
def listar_contas(request):
    if request.user.is_authenticated:
        contas = Conta.objects.filter(usuario=request.user)
        # TODO: Criar template listar_contas.html para exibir a lista de contas
        return render(request, 'listar_contas.html', {'contas': contas})

def criar_conta(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de conta
            form = ContaForm()
            # TODO: Criar template criar_conta.html para exibir o formulário
            return render(request, 'criar_conta.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova conta com os dados do formulário
            form = ContaForm(request.POST)
            if form.is_valid():
                conta = form.save(commit=False)
                conta.usuario = request.user
                conta.save()
                # TODO: Criar template conta_criada.html para exibir os detalhes da conta criada
                return render(request, 'conta_criada.html', {'conta': conta})

def ler_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            # TODO: Criar template ler_conta.html para exibir os detalhes da conta
            return render(request, 'ler_conta.html', {'conta': conta})
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'conta_nao_encontrada.html')

def atualizar_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            if request.method == 'GET':
                form = ContaForm(instance=conta)
                # TODO: Criar template atualizar_conta.html para exibir o formulário de atualização
                return render(request, 'atualizar_conta.html', {'form': form, 'conta': conta})
            if request.method == 'POST':
                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    # TODO: Criar template conta_atualizada.html para exibir os detalhes da conta atualizada
                    return render(request, 'conta_atualizada.html', {'conta': conta})
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'conta_nao_encontrada.html')

def deletar_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            conta.delete()
            return render(request, 'conta_deletada.html')
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'conta_nao_encontrada.html')

# CRUD de Transação
def listar_transacoes(request):
    if request.user.is_authenticated:
        transacoes = Transacao.objects.filter(usuario=request.user)
        # TODO: Criar template listar_transacoes.html para exibir a lista de transações
        return render(request, 'listar_transacoes.html', {'transacoes': transacoes})

def criar_transacao(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de transação
            form = TransacaoForm()
            # TODO: Criar template criar_transacao.html para exibir o formulário
            return render(request, 'criar_transacao.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova transação com os dados do formulário
            form = TransacaoForm(request.POST)
            if form.is_valid():
                transacao = form.save(commit=False)
                transacao.usuario = request.user
                transacao.save()
                # TODO: Criar template transacao_criada.html para exibir os detalhes da transação criada
                return render(request, 'transacao_criada.html', {'transacao': transacao})

def ler_transacao(request, transacao_id):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=transacao_id, usuario=request.user)
            # TODO: Criar template ler_transacao.html para exibir os detalhes da transação
            return render(request, 'ler_transacao.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            # TODO: Criar template transacao_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'transacao_nao_encontrada.html')

def atualizar_transacao(request, transacao_id):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=transacao_id, usuario=request.user)
            if request.method == 'GET':
                form = TransacaoForm(instance=transacao)
                # TODO: Criar template atualizar_transacao.html para exibir o formulário de atualização
                return render(request, 'atualizar_transacao.html', {'form': form, 'transacao': transacao})
            if request.method == 'POST':
                form = TransacaoForm(request.POST, instance=transacao)
                if form.is_valid():
                    form.save()
                    # TODO: Criar template transacao_atualizada.html para exibir os detalhes da transação atualizada
                    return render(request, 'transacao_atualizada.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            # TODO: Criar template transacao_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'transacao_nao_encontrada.html')

def deletar_transacao(request, transacao_id):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=transacao_id, usuario=request.user)
            transacao.delete()
            # TODO: Criar template transacao_deletada.html para exibir mensagem de sucesso
            return render(request, 'transacao_deletada.html')
        except Transacao.DoesNotExist:
            # TODO: Criar template transacao_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'transacao_nao_encontrada.html')

# CRUD de Categoria
def criar_categoria(request):
    pass

def ler_categoria(request, categoria_id):
    pass

def atualizar_categoria(request, categoria_id):
    pass

def deletar_categoria(request, categoria_id):
    pass
