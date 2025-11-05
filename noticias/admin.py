from django.contrib import admin
# Adicionamos 'ProgramaRadio' à importação
from .models import (
    Noticia, Categoria, ModoLeitura, LerMaisTarde, 
    Pesquisa, Comentario, ProgramaRadio
)

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

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'autor', 'data_criacao', 'conteudo')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('conteudo', 'autor__username', 'noticia__titulo')
    readonly_fields = ('noticia', 'autor', 'conteudo', 'data_criacao')

    def has_add_permission(self, request):
        return False

@admin.register(ProgramaRadio)
class ProgramaRadioAdmin(admin.ModelAdmin):
    """
    Painel para gerenciar a grade de programação da rádio.
    """
    list_display = ('horario_inicio', 'horario_fim', 'nome_programa', 'apresentador')
    search_fields = ('nome_programa', 'apresentador')