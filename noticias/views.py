from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError # Importe para a captura de erros
from django.contrib import messages 


# --- ALTERAÇÃO AQUI ---
# Adicionamos o novo modelo 'Comentario' à lista de importação
from .models import Noticia, LerMaisTarde, Pesquisa, SugestaoUser, Comentario

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

# --- TODA A LÓGICA DE COMENTÁRIOS FOI ADICIONADA AQUI ---
def detalhe_noticia(request, noticia_id):
    # 1. Busca a notícia (como já fazia antes)
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    # 2. Busca todos os comentários associados a esta notícia
    #    (Usando o 'related_name="comentarios"' que definimos no models.py)
    comentarios = noticia.comentarios.all()

    # 3. Lógica para processar um NOVO comentário (quando o formulário é enviado)
    if request.method == 'POST':
        # Apenas usuários logados podem comentar
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para enviar um comentário.")
        else:
            # Pega o texto do formulário. O 'name' do campo no HTML será 'conteudo'
            conteudo_comentario = request.POST.get('conteudo', '').strip()
            
            if conteudo_comentario:
                # Se o texto não for vazio, cria o comentário
                Comentario.objects.create(
                    noticia=noticia,
                    autor=request.user,
                    conteudo=conteudo_comentario
                )
                messages.success(request, "Seu comentário foi publicado!")
                # Redireciona para a mesma página para evitar reenvio do formulário
                return redirect('detalhe_noticia', noticia_id=noticia.id)
            else:
                # Se o texto estiver vazio, envia uma mensagem de erro
                messages.error(request, "O comentário não pode estar vazio.")

    # 4. Lógica para o botão "Salvar" (como já fazia antes)
    salvo_para_depois = False
    if request.user.is_authenticated:
        salvo_para_depois = LerMaisTarde.objects.filter(usuario=request.user, noticia=noticia).exists()
    
    # 5. Adiciona os comentários ao contexto que vai para o template
    contexto = { 
        'noticia': noticia, 
        'salvo_para_depois': salvo_para_depois,
        'comentarios': comentarios  # Envia a lista de comentários para o HTML
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