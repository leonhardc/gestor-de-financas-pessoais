from django.shortcuts import render
from .forms import CadastroUsuarioForm
from django.contrib.auth.models import User


def criar_usuario(request):
    if request.method == 'GET':
        formulario_cadastro = CadastroUsuarioForm()
        return render(request, 'usuarios/criar_usuario.html', {'form': formulario_cadastro})
    if request.method == 'POST':
        formulario_cadastro = CadastroUsuarioForm(request.POST)
        if formulario_cadastro.is_valid():
            # Aqui você pode criar o usuário usando os dados do formulário
            # Por exemplo, usando o modelo User do Django:            
            username = formulario_cadastro.cleaned_data['username']
            email = formulario_cadastro.cleaned_data['email']
            password = formulario_cadastro.cleaned_data['password1']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('usuario:login')  # Redireciona para a página de login após criar o usuário
        else:
            return render(request, 'usuarios/criar_usuario.html', {'form': formulario_cadastro})