
from django.contrib import admin
from django.urls import path
from app_crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Direcionar a raiz para a página de autenticação
    path('', views.autenticacao, name='home'),
    path('autenticacao/', views.autenticacao, name='autenticacao'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('interesse/', views.interesse, name='interesse'),
    path('controle-contatos/', views.controle_contatos, name='controle_contatos'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('clientes/<int:cliente_id>/', views.detalhe_cliente, name='detalhe_cliente'),
]
