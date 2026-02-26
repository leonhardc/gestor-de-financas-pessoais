from django.urls import path
from .views import *

app_name = "contas"

urlpatterns = [
    # Contas
    path("", listar_contas, name="listar_contas"),
    path("conta/nova/", criar_conta, name="nova_conta"),
    path("conta/<uuid:pk>/", ler_conta, name="ler_conta"),
    path("conta/<uuid:pk>/editar/", atualizar_conta, name="atualizar_conta"),
    path("conta/<uuid:pk>/excluir/", deletar_conta, name="deletar_conta"),
    # Transacoes
    path("transacoes", listar_transacoes, name="listar_transacoes"),
    path("transacao/nova/", criar_transacao, name="nova_transacao"),
    path("transacao/<uuid:pk>/", ler_transacao, name="ler_transacao"),
    path("transacao/<uuid:pk>/editar/", atualizar_transacao, name="atualizar_transacao"),
    path("transacao/<uuid:pk>/excluir/", deletar_transacao, name="deletar_transacao"),
    # Categorias
    path("categorias", listar_categorias, name="listar_categorias"),
    path("categoria/nova/", criar_categoria, name="nova_categoria"),
    path("categoria/<uuid:pk>/", ler_categoria, name="ler_categoria"),
    path("categoria/<uuid:pk>/editar/", atualizar_categoria, name="atualizar_categoria"),
    path("categoria/<uuid:pk>/excluir/", deletar_categoria, name="deletar_categoria"),
]