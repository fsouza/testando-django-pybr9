# -*- coding: utf-8 -*-
import mock
from django import forms as django_forms, test
from django.conf import settings
from django.forms import widgets

from loja.vitrine import forms, views


class PaginaDeContatoTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.factory = test.RequestFactory()

    def test_preenche_formulario_e_envia_email(self):
        dados = {
            "nome": "Francisco Souza",
            "email": "fss@corp.globo.com",
            "mensagem": "Gostei do notebook azul",
        }
        request = self.factory.post("/contato", dados)
        with mock.patch('loja.vitrine.mailer.EnviadorDeEmail.enviar_email') as enviar_email:
            views.Contato().post(request)
            enviar_email.assert_called_with(
                assunto=u"Contato pelo site",
                mensagem=u"Gostei do notebook azul",
                remetente=u"fss@corp.globo.com",
                destinatario=settings.EMAIL_ADMIN,
            )


class FormularioContatoTestCase(test.TestCase):

    def test_deve_ter_campo_nome(self):
        self.assertIn("nome", forms.Contato.base_fields)

    def test_nome_deve_ter_no_maximo_255_caracteres(self):
        field = forms.Contato.base_fields["nome"]
        self.assertEqual(255, field.max_length)

    def test_deve_ter_campo_email(self):
        self.assertIn("email", forms.Contato.base_fields)

    def test_campo_email_deve_aceitar_apenas_emails_validos(self):
        field = forms.Contato.base_fields["email"]
        self.assertIsInstance(field, django_forms.EmailField)

    def test_deve_ter_campo_mensagem(self):
        self.assertIn("mensagem", forms.Contato.base_fields)

    def test_mensagem_deve_usar_Textarea_como_widget(self):
        field = forms.Contato.base_fields["mensagem"]
        self.assertIsInstance(field.widget, widgets.Textarea)
