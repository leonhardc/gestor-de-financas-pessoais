from datetime import timezone
from django.shortcuts import redirect, render
from .models import Conta, Transacao, Categoria
from .forms import ContaForm, TransacaoForm, CategoriaForm


# CRUD de Conta
def listar_contas(request):
    if request.user.is_authenticated:
        contas = Conta.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_contas.html', {'contas': contas})

def criar_conta(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de conta
            form = ContaForm()
            return render(request, 'contas/form.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova conta com os dados do formulário
            form = ContaForm(request.POST)
            if form.is_valid():
                conta = form.save(commit=False)
                conta.usuario = request.user
                conta.save()
                return render(request, 'contas/detalhes_conta.html', {'conta': conta})

def ler_conta(request, uuid):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.filter(id=uuid, usuario=request.user).exists()
            if conta:
                conta = Conta.objects.get(id=uuid, usuario=request.user)
                return render(request, 'contas/detalhes_conta.html', {'conta': conta})
            else:
                return render(request, 'contas/conta_nao_encontrada.html', context={'conta': False})
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', context={'conta': False})

def atualizar_conta(request, uuid):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=uuid, usuario=request.user)
            if request.method == 'GET':
                form = ContaForm(instance=conta)
                return render(request, 'contas/form.html', {'form': form, 'conta': conta})
            if request.method == 'POST':
                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_conta.html', {'conta': conta})
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')

def deletar_conta(request, uuid):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=uuid, usuario=request.user)
            conta.delete()
            return redirect('contas:listar_contas')
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')

# CRUD de Transação
def listar_transacoes(request):
    if request.user.is_authenticated:
        transacoes = Transacao.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_transacoes.html', {'transacoes': transacoes})

def criar_transacao(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de transação
            form = TransacaoForm()
            return render(request, 'contas/form.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova transação com os dados do formulário
            form = TransacaoForm(request.POST)
            if form.is_valid():
                transacao = form.save(commit=False)
                transacao.usuario = request.user
                transacao.save()
                return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})

def ler_transacao(request, uuid):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=uuid, usuario=request.user)
            return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', context={'transacao': False})

def atualizar_transacao(request, uuid):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=uuid, usuario=request.user)
            if request.method == 'GET':
                form = TransacaoForm(instance=transacao)
                return render(request, 'contas/form.html', {'form': form, 'transacao': transacao})
            if request.method == 'POST':
                form = TransacaoForm(request.POST, instance=transacao)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', context={'transacao': False})

def deletar_transacao(request, uuid):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=uuid, usuario=request.user)
            transacao.delete()
            # TODO: Criar template transacao_deletada.html para exibir mensagem de sucesso
            return render(request, 'transacao_deletada.html')
        except Transacao.DoesNotExist:
            # TODO: Criar template transacao_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'transacao_nao_encontrada.html')

# CRUD de Categoria
def listar_categorias(request):
    if request.user.is_authenticated:
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_categorias.html', {'categorias': categorias})

def criar_categoria(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de categoria
            form = CategoriaForm()
            return render(request, 'contas/form.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova categoria com os dados do formulário
            form = CategoriaForm(request.POST)
            if form.is_valid():
                categoria = form.save(commit=False)
                categoria.usuario = request.user
                categoria.save()
                return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})

def ler_categoria(request, uuid):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=uuid, usuario=request.user)
            return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')

def atualizar_categoria(request, uuid):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=uuid, usuario=request.user)
            if request.method == 'GET':
                form = CategoriaForm(instance=categoria)
                return render(request, 'contas/form.html', {'form': form, 'categoria': categoria})
            if request.method == 'POST':
                form = CategoriaForm(request.POST, instance=categoria)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')

def deletar_categoria(request, uuid):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=uuid, usuario=request.user)
            categoria.delete()
            return render(request, 'contas/listar_categorias.html')
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
