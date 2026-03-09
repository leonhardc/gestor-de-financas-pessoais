from django.urls import path
from .views import *

app_name = "contas"

urlpatterns = [
    # Home
    path("", index, name="home"),
    # login e logout
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),
    # Contas
    path("contas/", listar_contas, name="listar_contas"),
    path("conta/nova/", criar_conta, name="nova_conta"),
    path("conta/<uuid:pk>/", ler_conta, name="ler_conta"),
    path("conta/<uuid:pk>/editar/", atualizar_conta, name="atualizar_conta"),
    path("conta/<uuid:pk>/excluir/", deletar_conta, name="deletar_conta"),
    # Transacoes
    path("transacoes/", listar_transacoes, name="listar_transacoes"),
    path("transacao/nova/", criar_transacao, name="nova_transacao"),
    path("transacao/<uuid:pk>", ler_transacao, name="ler_transacao"),
    path("transacao/<uuid:pk>/editar/", atualizar_transacao, name="atualizar_transacao"),
    path("transacao/<uuid:pk>/excluir/", deletar_transacao, name="deletar_transacao"),
    # Categorias
    path("categorias/", listar_categorias, name="listar_categorias"),
    path("categoria/nova/", criar_categoria, name="nova_categoria"),
    path("categoria/<uuid:pk>/", ler_categoria, name="ler_categoria"),
    path("categoria/<uuid:pk>/editar/", atualizar_categoria, name="atualizar_categoria"),
    path("categoria/<uuid:pk>/excluir/", deletar_categoria, name="deletar_categoria"),
    # Orcamento Mensal
    path("orcamentos/", listar_orcamentos, name="listar_orcamentos"),
    path("orcamento/novo/", criar_orcamento, name="novo_orcamento"),
    path("orcamento/<uuid:pk>", ler_orcamento, name="ler_orcamento"),
    path("orcamento/<uuid:pk>/editar/", atualizar_orcamento, name="atualizar_orcamento"),
    path("orcamento/<uuid:pk>/excluir/", deletar_orcamento, name="deletar_orcamento"),
    # Fechar mes
    path("fechar_mes/", fechar_mes, name="fechar_mes"),
    path("detalhes_mes/<int:ano>/<int:mes>/", detalhes_mes, name="detalhes_mes"),
    path("relatorios/", relatorios, name="relatorios"),
    path("relatorios/<uuid:id>/", relatorio_detalhe, name="relatorio_detalhe"),
]