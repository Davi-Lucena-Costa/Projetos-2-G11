# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Noticia
import time

class NoticiaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Configuração executada uma vez para toda a classe de teste.
        Use isso para criar objetos que não serão modificados por nenhum teste.
        """
        cls.noticia = Noticia.objects.create(
            titulo="Título de Teste",
            conteudo="Conteúdo de teste"
        )

    def test_criacao_basica_noticia(self):
        """
        Testa se os campos básicos foram salvos corretamente.
        """
        # self.noticia foi criado no setUpTestData
        self.assertEqual(self.noticia.titulo, "Título de Teste")
        self.assertEqual(self.noticia.conteudo, "Conteúdo de teste")
        self.assertTrue(Noticia.objects.exists())
        self.assertEqual(Noticia.objects.count(), 1)

    def test_representacao_str(self):
        """
        Testa o método __str__ do modelo (assumindo que ele retorna o título).
        """
        self.assertEqual(str(self.noticia), "Título de Teste")

    def test_data_publicacao_automatica(self):
        """
        Testa se um campo 'data_publicacao' (assumindo que existe 
        com auto_now_add=True) é definido automaticamente.
        """
        # Para esse teste, vamos criar uma nova notícia
        noticia_nova = Noticia.objects.create(
            titulo="Outro Título",
            conteudo="Outro conteúdo"
        )
        
        # Espera-se que a data de publicação seja definida
        self.assertIsNotNone(noticia_nova.data_publicacao) 
        # Espera-se que seja uma data próxima de "agora"
        self.assertAlmostEqual(
            noticia_nova.data_publicacao, 
            timezone.now(), 
            delta=timezone.timedelta(seconds=1)
        )

    def test_titulo_max_length(self):
        """
        Testa a restrição max_length do campo 'titulo'.
        (Assumindo que seu modelo tem: titulo = models.CharField(max_length=200))
        """
        # Tenta criar um título muito longo
        max_length = Noticia._meta.get_field('titulo').max_length
        titulo_longo = "a" * (max_length + 1)
        
        noticia_titulo_longo = Noticia(
            titulo=titulo_longo, 
            conteudo="Conteúdo qualquer"
        )
        
        # Deve levantar um ValidationError ao tentar validar o modelo
        with self.assertRaises(ValidationError):
            noticia_titulo_longo.full_clean()

    def test_titulo_nao_pode_ser_nulo(self):
        """
        Testa se o campo 'titulo' não pode ser nulo (assumindo null=False).
        """
        with self.assertRaises(IntegrityError):
            Noticia.objects.create(
                titulo=None,
                conteudo="Conteúdo sem título"
            )

    def test_conteudo_nao_pode_ser_vazio(self):
        """
        Testa se o campo 'conteudo' não pode ser vazio (assumindo blank=False).
        """
        noticia_sem_conteudo = Noticia(
            titulo="Título sem conteúdo",
            conteudo=""  # Conteúdo vazio
        )
        
        # Deve levantar um ValidationError ao validar
        with self.assertRaises(ValidationError):
            noticia_sem_conteudo.full_clean()

    