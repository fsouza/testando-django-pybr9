# -*- coding: utf-8 -*-
import mock
import splinter
from django import forms as django_forms, test
from django.conf import settings
from django.core import mail
from django.forms import widgets

from loja.vitrine import forms


class PaginaDeContatoTestCase(test.LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = splinter.Browser("firefox")
        super(PaginaDeContatoTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(PaginaDeContatoTestCase, cls).tearDownClass()

    def test_preenche_formulario_e_envia_email(self):
        self.browser.visit("%s/contato" % self.live_server_url)
        self.browser.fill("nome", "Francisco Souza")
        self.browser.fill("email", "fss@corp.globo.com")
        self.browser.fill("mensagem", "Gostei do notebook azul")
        self.browser.find_by_css("button").click()
        email = mail.outbox[0]
        self.assertEqual(u"Contato pelo site", email.subject)
        self.assertEqual(u"Gostei do notebook azul", email.body)
        self.assertEqual(u"fss@corp.globo.com", email.from_email)
        self.assertEqual([settings.EMAIL_ADMIN], email.to)


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

    @mock.patch("django.core.mail.send_mail")
    def test_envia_email(self, send_mail):
        dados = {
            "nome": "Francisco",
            "email": "fss@corp.globo.com",
            "mensagem": "Oi, tudo bem?",
        }
        form = forms.Contato(dados)
        form.enviar_email()
        send_mail.assert_called_with(subject="Contato pelo site",
                                     from_email="fss@corp.globo.com",
                                     message="Oi, tudo bem?",
                                     recipient_list=[settings.EMAIL_ADMIN])
