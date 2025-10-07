from django.db import models
from django.contrib.auth.models import User

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
        # Garante que um usuário não possa salvar a mesma notícia mais de uma vez
        unique_together = ('usuario', 'noticia')  

    def __str__(self):
        return f"{self.usuario.username} salvou '{self.noticia.titulo}'"