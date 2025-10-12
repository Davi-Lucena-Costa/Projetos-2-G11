# noticias/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('pesquisa/', views.pesquisar_noticias, name='pesquisar_noticias'),

    
    # URL para ver o detalhe de uma notícia (ex: /noticia/5/)
    path('noticia/<int:noticia_id>/', views.detalhe_noticia, name='detalhe_noticia'),

    # URL para a AÇÃO de salvar/remover
    path('noticia/<int:noticia_id>/salvar/', views.salvar_noticia, name='salvar_noticia'),
    
    # URL para a página que lista as notícias salvas
    path('salvos/', views.lista_salvos, name='lista_salvos'),
]