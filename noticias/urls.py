
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # HOME FUNCIONANDO

    path('esportes/', views.pagina_esportes, name='pagina_esportes'),
    path('politica/', views.pagina_politica, name='pagina_politica'),
    path('radio/', views.pagina_radio, name='pagina_radio'),
    path('pesquisar/', views.pesquisar_noticias, name='pesquisar_noticias'),
    path('salvos/', views.lista_salvos, name='lista_salvos'),
    path('noticia/<int:noticia_id>/', views.detalhe_noticia, name='detalhe_noticia'),
    path('categoria/<str:nome>/', views.noticias_por_categoria, name='noticias_por_categoria'),
    path('salvar/<int:noticia_id>/', views.salvar_noticia, name='salvar_noticia'),
    path('accounts/signup/', views.cadastrar_usuario, name='signup'),
]
