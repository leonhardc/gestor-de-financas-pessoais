from datetime import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .models import Conta, Transacao, Categoria
from .forms import ContaForm, TransacaoForm, CategoriaForm, LoginForm

# Index
def index(request):
    return render(request, 'index.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        contas = Conta.objects.filter(usuario=request.user)
        transacoes = Transacao.objects.filter(usuario=request.user)
        categorias = Categoria.objects.filter(usuario=request.user)
        receita_total = sum([transacao.valor for transacao in transacoes if transacao.tipo == 'receita'])
        despesa_total = sum([transacao.valor for transacao in transacoes if transacao.tipo == 'despesa'])
        saldo_total = receita_total - despesa_total
        return render(request, 'contas/dashboard.html', {'contas': contas, 
                                                         'transacoes': transacoes, 
                                                         'categorias': categorias, 
                                                         'receita_total': receita_total, 
                                                         'despesa_total': despesa_total, 
                                                         'saldo_total': saldo_total
                                                         }
                                                    )
    else:
        return redirect('contas:login')

# Operacoes de Login

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'contas/form.html', {'form': form, 'tipo': 'login'})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login_user = authenticate(request, username=username, password=password)
            if login_user is not None:
                auth_login(request, login_user)
                return redirect('contas:dashboard')
            else:
                form.add_error(None, 'Usuário ou senha inválidos')
                return render(request, 'contas/form.html', {'form': form, 'tipo': 'login'})
        else:
            return render(request, 'contas/form.html', {'form': form, 'tipo': 'login'})

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('contas:home')


# CRUD de Conta
def listar_contas(request):
    if request.user.is_authenticated:
        contas = Conta.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_contas.html', {'contas': contas})
    else:
        return redirect('contas:login')

def criar_conta(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de conta
            form = ContaForm()
            return render(request, 'contas/form.html', {'form': form,'tipo': 'conta', 'modo': 'criar'})
        if request.method == 'POST':
            # Lógica para criar uma nova conta com os dados do formulário
            form = ContaForm(request.POST)
            if form.is_valid():
                conta = form.save(commit=False)
                conta.usuario = request.user
                conta.save()
                return render(request, 'contas/detalhes_conta.html', {'conta': conta})
    else: 
        return redirect('contas:login')

def ler_conta(request, pk):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.filter(id=pk, usuario=request.user).exists()
            if conta:
                conta = Conta.objects.get(id=pk, usuario=request.user)
                return render(request, 'contas/detalhes_conta.html', {'conta': conta})
            else:
                return render(request, 'contas/conta_nao_encontrada.html', {'tipo': 'conta', 'modo': 'ler'})
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', {'tipo': 'conta', 'modo': 'ler'})
    else:
        return redirect('contas:login')

def atualizar_conta(request, pk):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=pk, usuario=request.user)
            if request.method == 'GET':
                form = ContaForm(instance=conta)
                return render(request, 'contas/form.html', {'form': form, 'tipo': 'conta', 'modo': 'editar'})
            if request.method == 'POST':
                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_conta.html', {'conta': conta,})
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

def deletar_conta(request, pk):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                conta = Conta.objects.get(id=pk, usuario=request.user)
                conta.delete()
                return redirect('contas:listar_contas')
            else :
                return redirect('contas:listar_contas')
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

# CRUD de Transação
def listar_transacoes(request):
    if request.user.is_authenticated:
        transacoes = Transacao.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_transacoes.html', {'transacoes': transacoes})
    else:
        return redirect('contas:login')

def criar_transacao(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de transação
            form = TransacaoForm()
            return render(request, 'contas/form.html', {'form': form, 'tipo': 'transacao', 'modo': 'criar'})
        if request.method == 'POST':
            # Lógica para criar uma nova transação com os dados do formulário
            form = TransacaoForm(request.POST)
            if form.is_valid():
                transacao = form.save(commit=False)
                transacao.usuario = request.user
                transacao.save()
                return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
    else:
        return redirect('contas:login')

def ler_transacao(request, pk):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=pk, usuario=request.user)
            return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', context={'transacao': False})
    else:
        return redirect('contas:login')

def atualizar_transacao(request, pk):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=pk, usuario=request.user)
            if request.method == 'GET':
                form = TransacaoForm(instance=transacao)
                return render(request, 'contas/form.html', {'form': form, 'transacao': transacao, 'tipo': 'transacao', 'modo': 'editar'})
            if request.method == 'POST':
                form = TransacaoForm(request.POST, instance=transacao)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
        except Transacao.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html', {'tipo': 'transacao', 'modo': 'ler'})
    else:
        return redirect('contas:login')

def deletar_transacao(request, pk):
    if request.user.is_authenticated:
        try:
            transacao = Transacao.objects.get(id=pk, usuario=request.user)
            transacao.delete()
            # TODO: Criar template transacao_deletada.html para exibir mensagem de sucesso
            return render(request, 'contas/listar_transacoes.html')
        except Transacao.DoesNotExist:
            # TODO: Criar template transacao_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'contas/conta_nao_encontrada.html', context={'transacao': False})

# CRUD de Categoria
def listar_categorias(request):
    if request.user.is_authenticated:
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_categorias.html', {'categorias': categorias})
    else:
        return redirect('contas:login')

def criar_categoria(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de categoria
            form = CategoriaForm()
            return render(request, 'contas/form.html', {'form': form, 'tipo': 'categoria', 'modo': 'criar'})
        if request.method == 'POST':
            # Lógica para criar uma nova categoria com os dados do formulário
            form = CategoriaForm(request.POST)
            if form.is_valid():
                categoria = form.save(commit=False)
                categoria.usuario = request.user
                categoria.save()
                return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
    else:
        return redirect('contas:login')

def ler_categoria(request, pk):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=pk, usuario=request.user)
            return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

def atualizar_categoria(request, pk):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=pk, usuario=request.user)
            if request.method == 'GET':
                form = CategoriaForm(instance=categoria)
                return render(request, 'contas/form.html', {'form': form, 'categoria': categoria, 'tipo': 'categoria', 'modo': 'editar'})
            if request.method == 'POST':
                form = CategoriaForm(request.POST, instance=categoria)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

def deletar_categoria(request, pk):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=pk, usuario=request.user)
            categoria.delete()
            return render(request, 'contas/listar_categorias.html')
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
       return redirect('contas:login')
