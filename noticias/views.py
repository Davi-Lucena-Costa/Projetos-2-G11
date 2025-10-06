from django.shortcuts import render

# noticias/views.py

from django.shortcuts import render
from .models import Noticia # Importa o seu modelo Noticia

def home(request):
    # Busca todas as notícias no banco de dados, ordenando pelas mais recentes
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao')
    
    # Define o contexto que será enviado para o HTML
    contexto = {
        'lista_de_noticias': ultimas_noticias
    }
    
    # Renderiza o arquivo home.html e envia o contexto para ele
    return render(request, 'home.html', contexto)
