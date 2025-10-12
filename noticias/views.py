from django.shortcuts import render
from django.db.models import Q

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

def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()
    resultados = []

    if termo:
        resultados = Noticia.objects.filter(
            Q(titulo__icontains=termo) | Q(subtitulo__icontains=termo)
        ).order_by('-data_publicacao')

    contexto = {
        'termo': termo,
        'resultados': resultados
    }

    return render(request, 'pesquisa.html', contexto)
