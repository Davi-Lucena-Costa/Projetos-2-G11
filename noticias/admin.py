from django.contrib import admin
# IMPORTANTE: Adicionamos o modelo 'Comentario' à importação
from .models import Noticia, Categoria, ModoLeitura, LerMaisTarde, Pesquisa, Comentario

# Para gerenciar o ModoLeitura dentro da própria Notícia
class ModoLeituraInline(admin.StackedInline):
    model = ModoLeitura
    can_delete = False
    verbose_name_plural = 'Modo de Leitura Simplificado'
    fk_name = 'noticia'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'data_publicacao')
    list_filter = ('data_publicacao', 'autor', 'categoria') 
    search_fields = ('titulo', 'conteudo', 'autor__username') 
    inlines = (ModoLeituraInline,)

@admin.register(LerMaisTarde)
class LerMaisTardeAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'usuario', 'salvo_em')
    list_filter = ('usuario', 'salvo_em')
    search_fields = ('usuario__username', 'noticia__titulo')

# Para gerenciar o histórico de Pesquisas no painel de Admin
@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    list_display = ('termo_buscado', 'usuario', 'data_busca')
    list_filter = ('data_busca', 'usuario')
    search_fields = ('termo_buscado', 'usuario__username')
    readonly_fields = ('termo_buscado', 'usuario', 'data_busca')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# --- NOVA CLASSE ADMIN ADICIONADA ---
# Para gerenciar e moderar os Comentários
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    # O que mostrar na lista de comentários
    list_display = ('noticia', 'autor', 'data_criacao', 'conteudo')
    
    # Como filtrar os comentários
    list_filter = ('data_criacao', 'autor')
    
    # Campos pelos quais podemos pesquisar
    search_fields = ('conteudo', 'autor__username', 'noticia__titulo')
    
    # Um admin não deve editar o comentário de um usuário, apenas aprovar ou apagar.
    # Por isso, tornamos os campos "somente leitura"
    readonly_fields = ('noticia', 'autor', 'conteudo', 'data_criacao')

    # Desabilita a opção de "Adicionar" um comentário manualmente pelo admin
    # (Comentários só podem ser criados pelo site)
    def has_add_permission(self, request):
        return False