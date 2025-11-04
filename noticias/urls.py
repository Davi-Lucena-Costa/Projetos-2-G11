# noticias/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('pesquisa/', views.pesquisar_noticias, name='pesquisar_noticias'),
    
    path('noticia/<int:noticia_id>/', views.detalhe_noticia, name='detalhe_noticia'),
    path('noticia/<int:noticia_id>/salvar/', views.salvar_noticia, name='salvar_noticia'),
    path('salvos/', views.lista_salvos, name='lista_salvos'),

    path('radio/', views.pagina_radio, name='pagina_radio'),
]