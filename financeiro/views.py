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
            return render(request, 'contas/forms.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova conta com os dados do formulário
            form = ContaForm(request.POST)
            if form.is_valid():
                conta = form.save(commit=False)
                conta.usuario = request.user
                conta.save()
                return render(request, 'contas/detalhes_conta.html', {'conta': conta})

def ler_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            return render(request, 'contas/detalhes_conta.html', {'conta': conta})
        except Conta.DoesNotExist:
            return render(request, 'contas/conta_nao_encontrada.html')

def atualizar_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            if request.method == 'GET':
                form = ContaForm(instance=conta)
                # TODO: Criar template atualizar_conta.html para exibir o formulário de atualização
                return render(request, 'contas/forms.html', {'form': form, 'conta': conta})
            if request.method == 'POST':
                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    # TODO: Criar template conta_atualizada.html para exibir os detalhes da conta atualizada
                    return render(request, 'contas/detalhes_conta.html', {'conta': conta})
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'contas/conta_nao_encontrada.html')

def deletar_conta(request, conta_id):
    if request.user.is_authenticated:
        try:
            conta = Conta.objects.get(id=conta_id, usuario=request.user)
            conta.delete()
            # TODO: Adicionar mensagem de conta deletada com sucesso
            # return render(request, 'conta_deletada.html')
            return redirect('contas:listar_contas')
        except Conta.DoesNotExist:
            # TODO: Criar template conta_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'contas/conta_nao_encontrada.html')

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
            return render(request, 'contas/forms.html', {'form': form})
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
                return render(request, 'contas/forms.html', {'form': form, 'transacao': transacao})
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
def listar_categorias(request):
    if request.user.is_authenticated:
        categorias = Categoria.objects.filter(usuario=request.user)
        # TODO: Criar template listar_categorias.html para exibir a lista de categorias
        return render(request, 'listar_categorias.html', {'categorias': categorias})

def criar_categoria(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Lógica para exibir o formulário de criação de categoria
            form = CategoriaForm()
            # TODO: Criar template criar_categoria.html para exibir o formulário
            return render(request, 'contas/forms.html', {'form': form})
        if request.method == 'POST':
            # Lógica para criar uma nova categoria com os dados do formulário
            form = CategoriaForm(request.POST)
            if form.is_valid():
                categoria = form.save(commit=False)
                categoria.usuario = request.user
                categoria.save()
                # TODO: Criar template categoria_criada.html para exibir os detalhes da categoria criada
                return render(request, 'categoria_criada.html', {'categoria': categoria})

def ler_categoria(request, categoria_id):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=categoria_id, usuario=request.user)
            # TODO: Criar template ler_categoria.html para exibir os detalhes da categoria
            return render(request, 'ler_categoria.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            # TODO: Criar template categoria_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'categoria_nao_encontrada.html')

def atualizar_categoria(request, categoria_id):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=categoria_id, usuario=request.user)
            if request.method == 'GET':
                form = CategoriaForm(instance=categoria)
                # TODO: Criar template atualizar_categoria.html para exibir o formulário de atualização
                return render(request, 'contas/forms.html', {'form': form, 'categoria': categoria})
            if request.method == 'POST':
                form = CategoriaForm(request.POST, instance=categoria)
                if form.is_valid():
                    form.save()
                    # TODO: Criar template categoria_atualizada.html para exibir os detalhes da categoria atualizada
                    return render(request, 'categoria_atualizada.html', {'categoria': categoria})
        except Categoria.DoesNotExist:
            # TODO: Criar template categoria_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'categoria_nao_encontrada.html')

def deletar_categoria(request, categoria_id):
    if request.user.is_authenticated:
        try:
            categoria = Categoria.objects.get(id=categoria_id, usuario=request.user)
            categoria.delete()
            # TODO: Criar template categoria_deletada.html para exibir mensagem de sucesso
            return render(request, 'categoria_deletada.html')
        except Categoria.DoesNotExist:
            # TODO: Criar template categoria_nao_encontrada.html para exibir mensagem de erro
            return render(request, 'categoria_nao_encontrada.html')
