from datetime import timezone
from django.shortcuts import render
from .models import Conta, Transacao, Categoria
from .forms import ContaForm, TransacaoForm, CategoriaForm


# CRUD de Conta
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
            if request.method == 'POST':
                conta.delete()
                # TODO: Criar template conta_deletada.html para exibir mensagem de sucesso
                return render(request, 'conta_deletada.html')
            # TODO: Criar template confirmar_delecao_conta.html para exibir confirmação de deleção
            return render(request, 'confirmar_delecao_conta.html', {'conta': conta})
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'conta_nao_encontrada.html')

# CRUD de Transação
def criar_transacao(request):
    pass

def ler_transacao(request, transacao_id):
    pass

def atualizar_transacao(request, transacao_id):
    pass

def deletar_transacao(request, transacao_id):
    pass

# CRUD de Categoria
def criar_categoria(request):
    pass

def ler_categoria(request, categoria_id):
    pass

def atualizar_categoria(request, categoria_id):
    pass

def deletar_categoria(request, categoria_id):
    pass
