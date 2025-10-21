from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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
        # Garante que um usuário não possa salvar a mesma notícia mais de uma vez
        unique_together = ('usuario', 'noticia')  

    def __str__(self):
        return f"{self.usuario.username} salvou '{self.noticia.titulo}'"

# --- NOVA CLASSE ADICIONADA ---
class Pesquisa(models.Model):
    termo_buscado = models.CharField(max_length=255)
    data_busca = models.DateTimeField(auto_now_add=True)
    
    # Este campo é opcional, permitindo pesquisas anônimas.
    # Se um usuário for deletado, a pesquisa dele fica associada a um usuário "nulo".
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.usuario:
            return f"'{self.termo_buscado}' por {self.usuario.username}"
        return f"'{self.termo_buscado}' (anônimo)"
        
    class Meta:
        # Ordena o histórico de pesquisas do mais recente para o mais antigo
        ordering = ['-data_busca']
        # Nome mais amigável para a área de administração do Django
        verbose_name_plural = "Histórico de Pesquisas"



# Obtém o modelo de usuário ativo no projeto
User = get_user_model() 



class SugestaoUser(models.Model):
    # Campo de texto principal da sugestão
    texto = models.TextField(verbose_name="Texto da Sugestão")
    
    # Usuário que sugeriu (pode ser nulo/anônimo)
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Usuário (opcional)"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    # *************************************************************
    # LÓGICA DE VALIDAÇÃO (Método Estático)
    # *************************************************************
    @staticmethod
    def validar_Sugestao(texto):
        texto = texto.strip()  

        
        texto_lower = texto.lower() 

        if len(texto) < 4:
            raise ValidationError("Susgestão muito curta. Digite pelo menos 4 caracteres.")
        

        palavras_proibidas = ['crimes', 'spam', 'sem sentido', 'venda_ilegal']
        for palavra in palavras_proibidas:
            if palavra in texto_lower:
                raise ValidationError("A sugestão contém uma palavra inválida: por favor seja mais específico")
        
        return texto
    # *************************************************************
    
    def __str__(self):
        # Retorna os primeiros 50 caracteres da sugestão para representação em string
        return self.texto[:50]  

    class Meta:
        verbose_name = "Sugestão de Usuário"
        verbose_name_plural = "Sugestões de Usuários"