# noticias/urls.py (URLS DENTRO DE NOTICIAS)

from django.urls import path
from . import views # Importa as views da sua app

urlpatterns = [
    # Quando a URL for vazia (homepage), chame a função 'home' da views.py
    path('', views.home, name='home'), 
    path('pesquisa/', views.pesquisar_noticias, name='pesquisar_noticias'),
]