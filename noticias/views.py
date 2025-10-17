# noticias/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# IMPORTANTE: Adicione o modelo 'Pesquisa' aqui
from .models import Noticia, LerMaisTarde, Pesquisa

def home(request):
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao')
    contexto = { 'lista_de_noticias': ultimas_noticias }
    # CORREÇÃO AQUI: (Sua correção já estava certa, mantive)
    return render(request, 'noticias/home.html', contexto)

def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()
    resultados = []

    # Só execute a busca e salve se o termo não for vazio
    if termo:
        # --- LÓGICA PARA SALVAR O HISTÓRICO DA BUSCA ---
        # Cria um novo objeto Pesquisa com o termo buscado
        nova_pesquisa = Pesquisa(termo_buscado=termo)
        # Se o usuário estiver logado, associe a pesquisa a ele
        if request.user.is_authenticated:
            nova_pesquisa.usuario = request.user
        # Salva o registro no banco de dados
        nova_pesquisa.save()
        # --- FIM DA NOVA LÓGICA ---

        # A sua lógica de busca continua a mesma aqui
        resultados = Noticia.objects.filter(
            Q(titulo__icontains=termo) | Q(conteudo__icontains=termo)
        ).distinct().order_by('-data_publicacao')

    contexto = { 'termo': termo, 'resultados': resultados }
    # CORREÇÃO AQUI: (Sua correção já estava certa, mantive)
    return render(request, 'noticias/pesquisa.html', contexto)

def detalhe_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    salvo_para_depois = False
    if request.user.is_authenticated:
        salvo_para_depois = LerMaisTarde.objects.filter(usuario=request.user, noticia=noticia).exists()
    contexto = { 'noticia': noticia, 'salvo_para_depois': salvo_para_depois }
    
    return render(request, 'noticias/detalhe.html', contexto)

@login_required
def salvar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    registro, criado = LerMaisTarde.objects.get_or_create(usuario=request.user, noticia=noticia)
    if not criado:
        registro.delete()
    return redirect('detalhe_noticia', noticia_id=noticia.id)

@login_required
def lista_salvos(request):
    itens_salvos = LerMaisTarde.objects.filter(usuario=request.user)
    contexto = {'itens_salvos': itens_salvos}
    
    return render(request, 'noticias/salvos.html', contexto)