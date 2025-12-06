# noticias/context_processors.py

from .models import Noticia

def noticia_mais_recente(request):
    """
    Context processor que adiciona a notícia mais recente a todos os templates.
    """
    try:
        noticia_recente = Noticia.objects.order_by('-data_publicacao').first()
    except:
        noticia_recente = None
    
    return {
        'noticia_mais_recente': noticia_recente
    }
