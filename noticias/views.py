from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError # Importe para a captura de erros
from django.contrib import messages 


# Todos os seus modelos agora são importados do mesmo lugar.
from .models import Noticia, LerMaisTarde, Pesquisa, SugestaoUser

def home(request):
    
 
    dados_sugestao = {
        'texto_sugerido': '', # Começa vazio
        'erro': None
    }

    if request.method == 'POST':
        # Verificamos se o POST é do formulário de sugestão
        if 'sugestao_texto' in request.POST:
            texto_brut = request.POST.get('sugestao_texto')
            dados_sugestao['texto_sugerido'] = texto_brut # Guarda o texto digitado
            
            usuario = request.user if request.user.is_authenticated else None
            
            try:
                # 1. Crie a instância do modelo
                sugestao = SugestaoUser(texto=texto_brut, usuario=usuario)
                
                # 2. Rode o método clean() que está no models.py
                sugestao.full_clean() 
                
                # 3. Se a validação passar, salve no banco
                sugestao.save()

                messages.success(request, "Sugestão enviada com sucesso! Obrigado :)")
                return redirect('home') # Redireciona para a home
            
            except ValidationError as e:
                # Pega a(s) mensagem(ns) de erro do 'clean()'
                dados_sugestao['erro'] = e.messages[0] if e.messages else "Erro de validação."
                messages.error(request, f"Erro ao enviar sugestão: {dados_sugestao['erro']}")
    
    # A lógica de buscar notícias continua a mesma
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao')
    
    contexto = { 
        'lista_de_noticias': ultimas_noticias,
        'sugestao': dados_sugestao # Envia os dados do formulário para o template
    }
    
    # Renderiza a home page
    return render(request, 'noticias/home.html', contexto)

def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()
    resultados = []

    if termo:
        nova_pesquisa = Pesquisa(termo_buscado=termo)
        if request.user.is_authenticated:
            nova_pesquisa.usuario = request.user
        nova_pesquisa.save()

        resultados = Noticia.objects.filter(
            Q(titulo__icontains=termo) | Q(conteudo__icontains=termo)
        ).distinct().order_by('-data_publicacao')

    contexto = { 'termo': termo, 'resultados': resultados }
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

