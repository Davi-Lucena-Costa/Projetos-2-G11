from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import CadastroForm
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
        texto_brut = request.POST.get('sugestao_texto', '').strip()
        dados_sugestao['texto_sugerido'] = texto_brut

        if not texto_brut:
            dados_sugestao['erro'] = "A sugestão não pode estar vazia."
            messages.error(request, "A sugestão não pode estar vazia.")
        else:
            usuario = request.user if request.user.is_authenticated else None
            sugestao = SugestaoUser(texto=texto_brut, usuario=usuario)

            try:
                sugestao.full_clean()
                sugestao.save()
                messages.success(request, "Sugestão enviada com sucesso! Obrigado :)")
                return redirect('home')
            except ValidationError as e:
                dados_sugestao['erro'] = e.messages[0]
                messages.error(request, dados_sugestao['erro'])

    contexto = {
        'lista_de_noticias': Noticia.objects.all().order_by('-data_publicacao'),
        'sugestao': dados_sugestao
    }
    return render(request, 'noticias/home.html', contexto)


def cadastrar_usuario(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Agora faça login.")
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'registration/signup.html', {"form": form})


def pesquisar_noticias(request):
    termo = request.GET.get('q', '').strip()
    if not termo:
        messages.error(request, "Digite algo para pesquisar.")
        return redirect('home')

    resultados = Noticia.objects.filter(
        Q(titulo__icontains=termo) | Q(conteudo__icontains=termo)
    ).distinct().order_by('-data_publicacao')

    if resultados.exists():
        nova_pesquisa = Pesquisa(termo_buscado=termo)
        if request.user.is_authenticated:
            nova_pesquisa.usuario = request.user
        nova_pesquisa.save()

    return render(request, 'noticias/pesquisa.html', {
        'termo': termo,
        'resultados': resultados
    })


def detalhe_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comentarios = noticia.comentarios.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para enviar um comentário.")
        else:
            conteudo = request.POST.get('conteudo', '').strip()
            if conteudo:
                Comentario.objects.create(
                    noticia=noticia, autor=request.user, conteudo=conteudo
                )
                messages.success(request, "Seu comentário foi publicado!")
                return redirect('detalhe_noticia', noticia_id=noticia.id)
            else:
                messages.error(request, "O comentário não pode estar vazio.")

    salvo = False
    if request.user.is_authenticated:
        salvo = LerMaisTarde.objects.filter(usuario=request.user, noticia=noticia).exists()

    return render(request, 'noticias/detalhe.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'salvo_para_depois': salvo
    })


@login_required
def salvar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    registro, criado = LerMaisTarde.objects.get_or_create(
        usuario=request.user, noticia=noticia
    )
    if not criado:
        registro.delete()
    return redirect('detalhe_noticia', noticia_id=noticia.id)


@login_required
def lista_salvos(request):
    itens = LerMaisTarde.objects.filter(usuario=request.user)
    return render(request, 'noticias/salvos.html', {'itens_salvos': itens})


def pagina_radio(request):
    agora = datetime.now().time()
    programacao = ProgramaRadio.objects.all()

    programa_atual = next(
        (p for p in programacao if p.horario_inicio <= agora <= p.horario_fim),
        None
    )

    return render(request, 'noticias/radio.html', {
        'programacao': programacao,
        'programa_atual': programa_atual
    })