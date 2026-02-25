from django.urls import path
# from .views import listar_contas, criar_conta, ler_conta, atualizar_conta, deletar_conta
from .views import *

app_name = "contas"

urlpatterns = [
    # Contas
    path("", listar_contas, name="lista"),
    path("conta/nova/", criar_conta, name="nova_conta"),
    path("conta/<uuid:pk>/", ler_conta, name="ler_conta"),
    path("conta/<uuid:pk>/editar/", atualizar_conta, name="editar_conta"),
    path("conta/<uuid:pk>/excluir/", deletar_conta, name="excluir_conta"),
    # Transacoes
    path("transacoes", listar_transacoes, name="listar_transacoes"),
    path("transacao/nova/", criar_transacao, name="nova_transacao"),
    path("transacao/<uuid:pk>/", ler_transacao, name="ler_transacao"),
    path("transacao/<uuid:pk>/editar/", atualizar_transacao, name="editar_transacao"),
    path("transacao/<uuid:pk>/excluir/", deletar_transacao, name="excluir_transacao"),
    # Categorias
]