from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 

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
        ordering = ['-data_publicacao']

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
        super().clean()
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
        self.texto = texto

    def __str__(self):
        return self.texto[:50]

class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=500)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f"Comentário de {self.autor.username} em '{self.noticia.titulo[:20]}...'"

class ProgramaRadio(models.Model):
    nome_programa = models.CharField(max_length=200)
    apresentador = models.CharField(max_length=200, blank=True)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    audio = models.FileField(upload_to='programas_radio/', blank=True, null=True)

    class Meta:
        ordering = ['horario_inicio']
        verbose_name = "Programa de Rádio"
        verbose_name_plural = "Programação da Rádio"

    def __str__(self):
        return f"{self.horario_inicio} - {self.nome_programa}"

