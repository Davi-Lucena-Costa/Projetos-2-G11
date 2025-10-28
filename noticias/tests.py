from django.test import TestCase
from .models import Noticia  

class NoticiaModelTest(TestCase):

    def setUp(self):
        self.noticia = Noticia.objects.create(
            titulo="Título de Teste",
            conteudo="Conteúdo de teste"
        )

    def test_criacao_noticia(self):
        self.assertEqual(self.noticia.titulo, "Título de Teste")
        self.assertEqual(self.noticia.conteudo, "Conteúdo de teste")
