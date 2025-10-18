from django.db import models
from django.core.exceptions import ValidationError  #ValidationError importado para validações personalizadas


# Create your models here.
class SugestaoUser(models.model):
    texto = models.CharField(max_length=80)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    data_da_sugestao = models.DateTimeField(auto_now_add=True)  



#Método para validação do conteúdo... (Limpeza básica)

@staticmethod
def validar_Sugestao(texto):
    texto = texto.strip()  
    texto_lower = texto.lower() 

    if len(texto) < 4:
        raise ValidationError("Susgestão muito curta. Digite pelo menos 4 caracteres.")
    

#Lógica de bloqueio para palavras ofensivas

    palavras_proibidas = ['crimes', 'spam', 'sem sentido', 'venda_ilegal']
    for palavra in palavras_proibidas:
        if palavra in texto_lower:
            raise ValidationError("A sugestão contém uma palavra inválida: por favor seja mais específico")
    


    return texto

def __str__(self):

    return self.texto[:50]  # Retorna os primeiros 50 caracteres da sugestão para representação em string   
