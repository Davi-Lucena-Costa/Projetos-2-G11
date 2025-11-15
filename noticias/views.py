from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages 

# Adicionamos 'ProgramaRadio' à importação
from .models import (
    Noticia, LerMaisTarde, Pesquisa, SugestaoUser, 
    Comentario, ProgramaRadio
)

def home(request):
    dados_sugestao = {
        'texto_sugerido': '',
        'erro': None
    }

    if request.method == 'POST':
        if 'sugestao_texto' in request.POST:
            texto_brut = request.POST.get('sugestao_texto')
            dados_sugestao['texto_sugerido'] = texto_brut
            
            usuario = request.user if request.user.is_authenticated else None
            
            try:
                sugestao = SugestaoUser(texto=texto_brut, usuario=usuario)
                sugestao.full_clean() 
                sugestao.save()
                messages.success(request, "Sugestão enviada com sucesso! Obrigado :)")
                return redirect('home')
            
            except ValidationError as e:
                dados_sugestao['erro'] = e.messages[0] if e.messages else "Erro de validação."
                messages.error(request, f"Erro ao enviar sugestão: {dados_sugestao['erro']}")
    
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao')
    
    contexto = { 
        'lista_de_noticias': ultimas_noticias,
        'sugestao': dados_sugestao
    }
    
    return render(request, 'noticias/home.html', contexto)

def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()

    # Se estiver vazio, dá feedback e volta pra home
    if not termo:
        messages.error(request, "Digite algo para pesquisar.")
        return redirect('home')

    # Se tiver termo, salva e busca normalmente
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
    comentarios = noticia.comentarios.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para enviar um comentário.")
        else:
            conteudo_comentario = request.POST.get('conteudo', '').strip()
            
            if conteudo_comentario:
                Comentario.objects.create(
                    noticia=noticia,
                    autor=request.user,
                    conteudo=conteudo_comentario
                )
                messages.success(request, "Seu comentário foi publicado!")
                return redirect('detalhe_noticia', noticia_id=noticia.id)
            else:
                messages.error(request, "O comentário não pode estar vazio.")

    salvo_para_depois = False
    if request.user.is_authenticated:
        salvo_para_depois = LerMaisTarde.objects.filter(usuario=request.user, noticia=noticia).exists()
    
    contexto = { 
        'noticia': noticia, 
        'salvo_para_depois': salvo_para_depois,
        'comentarios': comentarios
    }
    
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

def pagina_radio(request):
    """
    Exibe o player da rádio e a grade de programação do dia.
    """
    # Busca a programação e já ordena pela hora de início (definido no modelo)
    programacao = ProgramaRadio.objects.all()
    
    contexto = {
        'programacao': programacao
    }

    return render(request, 'noticias/radio.html', contexto)