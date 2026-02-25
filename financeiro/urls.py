from django.urls import path
from .views import listar_contas, criar_conta, ler_conta, atualizar_conta, deletar_conta

app_name = "contas"

urlpatterns = [
    path("", listar_contas, name="lista"),
    path("conta/nova/", criar_conta, name="nova_conta"),
    path("conta/<uuid:pk>/", ler_conta, name="ler_conta"),
    path("conta/<uuid:pk>/editar/", atualizar_conta, name="editar_conta"),
    path("conta/<uuid:pk>/excluir/", deletar_conta, name="excluir_conta"),
]