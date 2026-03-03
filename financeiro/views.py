from datetime import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .models import Conta, Transacao, Categoria, OrcamentoMensal
from .forms import ContaForm, TransacaoForm, CategoriaForm, LoginForm, OrcamentoMensalForm
from django.db.models import Sum
from django.db.models.functions import TruncDay
from datetime import date

# Index
def index(request):
    return render(request, 'index.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        # Gerando dados para os graficos do dashboard de pizza de gastos por categoria
        despesas_por_categoria = (
            Transacao.objects
            .filter(usuario=request.user, tipo='despesa')
            .values('categoria__nome')
            .annotate(total=Sum('valor'))
            .order_by('-total')   
        )

        labels = [item['categoria__nome'] for item in despesas_por_categoria]
        valores = [item['total'] for item in despesas_por_categoria]
        # Gerando dados para grafico de linha de despesas e receitas mensais
        hoje = date.today()
    
        transacoes = Transacao.objects.filter(
            usuario=request.user,
            data__year=hoje.year,
            data__month=hoje.month
        )

        receitas = (
            transacoes
            .filter(tipo='receita')
            .annotate(dia=TruncDay('data'))
            .values('dia')
            .annotate(total=Sum('valor'))
            .order_by('dia')
        )

        despesas = (
            transacoes
            .filter(tipo='despesa')
            .annotate(dia=TruncDay('data'))
            .values('dia')
            .annotate(total=Sum('valor'))
            .order_by('dia')
        )

        receitas_dict = {r['dia'].day: float(r['total']) for r in receitas}
        despesas_dict = {d['dia'].day: float(d['total']) for d in despesas}

        dias = list(range(1, 32))

        receitas_lista = [receitas_dict.get(dia, 0) for dia in dias]
        despesas_lista = [despesas_dict.get(dia, 0) for dia in dias]
        orcamentos = OrcamentoMensal.objects.filter(usuario=request.user, ano=hoje.year, mes=hoje.month)
        # Outros dados...
        contas = Conta.objects.filter(usuario=request.user)
        transacoes = Transacao.objects.filter(usuario=request.user)
        # # Ultimas 10 transacoes #
        ultimas_transacoes = (
            Transacao.objects
            .filter(usuario=request.user)
            .select_related('categoria', 'conta')
            .order_by('-data', '-id')[:10]
        )
        categorias = Categoria.objects.filter(usuario=request.user)
        receita_total = sum([transacao.valor for transacao in transacoes if transacao.tipo == 'receita'])
        despesa_total = sum([transacao.valor for transacao in transacoes if transacao.tipo == 'despesa'])
        saldo_total = sum([conta.saldo_atual for conta in contas])
        
        # Contexto para o template do dashboard
        contexto = {
            'contas': contas,
            'saldo_total': saldo_total,
            'transacoes': transacoes, 
            'categorias': categorias, 
            'receita_total': receita_total, 
            'despesa_total': despesa_total, 
            'saldo_total': saldo_total,
            'labels': labels,
            'valores': valores,
            'dias': dias,
            'receitas': receitas_lista,
            'despesas': despesas_lista,
            'ultimas_transacoes': ultimas_transacoes,
            'orcamentos': orcamentos,
        }

        return render(request, 'contas/dashboard.html', contexto)
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
        saldo_total = sum([conta.saldo_atual for conta in contas])  
        saldo_inicial_total = sum([conta.saldo_inicial for conta in contas])
        return render(request, 'contas/listar_contas.html', {'contas': contas, 'saldo_total': saldo_total, 'saldo_inicial_total': saldo_inicial_total})
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
                # return render(request, 'contas/detalhes_conta.html', {'conta': conta})
                return redirect('contas:listar_contas')
            else:
                return render(request, 'contas/form.html', {'form': form,'tipo': 'conta', 'modo': 'criar'})
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
                # return render(request, 'contas/detalhes_transacao.html', {'transacao': transacao})
                return redirect('contas:listar_transacoes')
            else:
                return render(request, 'contas/form.html', {'form': form, 'tipo': 'transacao', 'modo': 'criar'})
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
            if request.method == 'POST':
                transacao = Transacao.objects.get(id=pk, usuario=request.user)
                transacao.delete()
                return render(request, 'contas/listar_transacoes.html')
            else:
                return redirect('contas:listar_transacoes')
        except Transacao.DoesNotExist:
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
                # return render(request, 'contas/detalhes_categoria.html', {'categoria': categoria})
                return redirect('contas:listar_categorias')
            else:
                return render(request, 'contas/form.html', {'form': form, 'tipo': 'categoria', 'modo': 'criar'})
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
            if request.method == 'POST':
                categoria = Categoria.objects.get(id=pk, usuario=request.user)
                categoria.delete()
                return redirect('contas:listar_categorias')
            else:
                return redirect('contas:listar_categorias')
        except Categoria.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
       return redirect('contas:login')

# CRUD de OrcamentoMensal

def listar_orcamentos(request):
    if request.user.is_authenticated:
        orcamentos = OrcamentoMensal.objects.filter(usuario=request.user)
        return render(request, 'contas/listar_orcamentos.html', {'orcamentos': orcamentos})
    else:
        return redirect('contas:login')

def criar_orcamento(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = OrcamentoMensalForm()
            return render(request, 'contas/form.html', {'form': form, 'tipo': 'orcamento', 'modo': 'criar'})
        if request.method == 'POST':
            form = OrcamentoMensalForm(request.POST)
            if form.is_valid():
                orcamento = form.save(commit=False)
                orcamento.usuario = request.user
                orcamento.save()
                # return render(request, 'contas/detalhes_orcamento.html', {'orcamento': orcamento})
                return redirect('contas:listar_orcamentos')
            else:
                return render(request, 'contas/form.html', {'form': form, 'tipo': 'orcamento', 'modo': 'criar'})
    else:
        return redirect('contas:login')

def ler_orcamento(request, pk):
    if request.user.is_authenticated:
        try:
            orcamento = OrcamentoMensal.objects.get(id=pk, usuario=request.user)
            transacoes_por_categoria_despesa = Transacao.objects.filter(usuario=request.user, tipo='despesa', categoria=orcamento.categoria, data__year=orcamento.ano, data__month=orcamento.mes)
            total_despesas = sum([transacao.valor for transacao in transacoes_por_categoria_despesa])
            saldo = orcamento.valor_orcado - total_despesas
            return render(request, 'contas/detalhes_orcamento.html', {'orcamento': orcamento, 'total': total_despesas, 'saldo': saldo})
        except OrcamentoMensal.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

def atualizar_orcamento(request, pk):
    if request.user.is_authenticated:
        try:
            orcamento = OrcamentoMensal.objects.get(id=pk, usuario=request.user)
            if request.method == 'GET':
                form = OrcamentoMensalForm(instance=orcamento)
                return render(request, 'contas/form.html', {'form': form, 'orcamento': orcamento, 'tipo': 'orcamento', 'modo': 'editar'})
            if request.method == 'POST':
                form = OrcamentoMensalForm(request.POST, instance=orcamento)
                if form.is_valid():
                    form.save()
                    return render(request, 'contas/detalhes_orcamento.html', {'orcamento': orcamento})
        except OrcamentoMensal.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')

def deletar_orcamento(request, pk):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                orcamento = OrcamentoMensal.objects.get(id=pk, usuario=request.user)
                orcamento.delete()
                return redirect('contas:listar_orcamentos')
            else:
                return redirect('contas:listar_orcamentos')
        except OrcamentoMensal.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')
    else:
        return redirect('contas:login')
