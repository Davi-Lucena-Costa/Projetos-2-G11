# noticias/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Noticia, LerMaisTarde 

def home(request):
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao')
    contexto = {
        'lista_de_noticias': ultimas_noticias
    }
    return render(request, 'home.html', contexto)

# SUA VIEW DE PESQUISA (COM AJUSTE)
def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()
    resultados = []

    if termo:
        # PONTO DE ATENÇÃO: Removi a busca por 'subtitulo' que causaria um erro.
        resultados = Noticia.objects.filter(
            Q(titulo__icontains=termo) | Q(conteudo__icontains=termo)
        ).order_by('-data_publicacao')

    contexto = {
        'termo': termo,
        'resultados': resultados
    }
    return render(request, 'pesquisa.html', contexto)


# View para a página de detalhes de uma notícia
def detalhe_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    salvo_para_depois = False
    if request.user.is_authenticated:
        salvo_para_depois = LerMaisTarde.objects.filter(usuario=request.user, noticia=noticia).exists()

    contexto = {
        'noticia': noticia,
        'salvo_para_depois': salvo_para_depois
    }
    return render(request, 'detalhe.html', contexto) 

# View para a AÇÃO de salvar/remover (requer login)
@login_required
def salvar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    registro, criado = LerMaisTarde.objects.get_or_create(usuario=request.user, noticia=noticia)

    if not criado: # Se já existia, apague
        registro.delete()

    return redirect('detalhe_noticia', noticia_id=noticia.id)

# View para a página de notícias salvas (requer login)
@login_required
def lista_salvos(request):
    itens_salvos = LerMaisTarde.objects.filter(usuario=request.user)
    contexto = {'itens_salvos': itens_salvos}
    return render(request, 'salvos.html', contexto) 