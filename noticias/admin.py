from django.contrib import admin
from .models import Noticia, Categoria, ModoLeitura, LerMaisTarde

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