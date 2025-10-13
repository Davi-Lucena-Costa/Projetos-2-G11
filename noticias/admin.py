from django.contrib import admin
# IMPORTANTE: Adicione o modelo 'Pesquisa' aqui
from .models import Noticia, Categoria, ModoLeitura, LerMaisTarde, Pesquisa

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

# --- NOVA CLASSE ADMIN ADICIONADA ---
# Para gerenciar o histórico de Pesquisas no painel de Admin
@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    list_display = ('termo_buscado', 'usuario', 'data_busca')
    list_filter = ('data_busca', 'usuario')
    search_fields = ('termo_buscado', 'usuario__username')
    # Torna o painel 'somente leitura', já que não faz sentido editar um histórico de busca
    readonly_fields = ('termo_buscado', 'usuario', 'data_busca')

    # Desabilita a opção de adicionar novas pesquisas manualmente pelo admin
    def has_add_permission(self, request):
        return False

    # Desabilita a opção de deletar pesquisas pelo admin (opcional, mas recomendado)
    def has_delete_permission(self, request, obj=None):
        return False