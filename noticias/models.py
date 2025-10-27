# noticias/models.py

from django.db import models
from django.contrib.auth.models import User
# ADICIONAMOS A IMPORTAÇÃO DE VALIDATIONERROR
from django.core.exceptions import ValidationError 

# Modelo para as categorias das notícias
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(help_text="Conteúdo completo da notícia, com HTML, imagens, etc.")
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-data_publicacao'] # Ordena as notícias da mais nova para a mais antiga

class ModoLeitura(models.Model):
    noticia = models.OneToOneField(
        Noticia, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    conteudo_simplificado = models.TextField(
        help_text="Versão do texto puro, sem formatação ou imagens."
    )

    def __str__(self):
        return f"Modo de Leitura para: {self.noticia.titulo}"

class LerMaisTarde(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    salvo_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'noticia')  

    def __str__(self):
        return f"{self.usuario.username} salvou '{self.noticia.titulo}'"

class Pesquisa(models.Model):
    termo_buscado = models.CharField(max_length=255)
    data_busca = models.DateTimeField(auto_now_add=True)
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.usuario:
            return f"'{self.termo_buscado}' por {self.usuario.username}"
        return f"'{self.termo_buscado}' (anônimo)"
        
    class Meta:
        ordering = ['-data_busca']
        verbose_name_plural = "Histórico de Pesquisas"


class SugestaoUser(models.Model):
    texto = models.CharField(max_length=80)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    data_da_sugestao = models.DateTimeField(auto_now_add=True) 


    def clean(self):
        super().clean() # Chama a validação padrão primeiro

        if not self.texto:
            raise ValidationError("A sugestão não pode estar vazia.")

        texto = self.texto.strip()  
        texto_lower = texto.lower() 

        if len(texto) < 4:
            raise ValidationError("Sugestão muito curta. Digite pelo menos 4 caracteres.")
        
        palavras_proibidas = ['crimes', 'spam', 'sem sentido', 'venda_ilegal']
        for palavra in palavras_proibidas:
            if palavra in texto_lower:
                raise ValidationError("A sugestão contém uma palavra inválida: por favor seja mais específico")
        
        self.texto = texto # Salva o texto limpo (sem espaços extras)

    def __str__(self):
        return self.texto[:50] # Retorna os primeiros 50 caracteres 

# --- NOVA CLASSE ADICIONADA ---
# Modelo para os comentários das notícias
class Comentario(models.Model):
    # Relação com a Notícia: se a notícia é apagada, os comentários somem.
    # related_name='comentarios' permite que a gente acesse noticia.comentarios.all()
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    
    # Relação com o Autor: se o usuário é apagado, seus comentários somem.
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # O texto do comentário
    conteudo = models.TextField(max_length=500)
    
    # Data de criação (definida automaticamente quando o comentário é salvo)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ordena os comentários do mais antigo para o mais novo (ordem de leitura)
        ordering = ['data_criacao']

    def __str__(self):
        # Um texto útil para vermos no painel de administração
        return f"Comentário de {self.autor.username} em '{self.noticia.titulo[:20]}...'"