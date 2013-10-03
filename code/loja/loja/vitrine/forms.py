from django import forms
from django.conf import settings
from django.core import mail
from django.forms import widgets


class Contato(forms.Form):
    nome = forms.CharField(max_length=255)
    email = forms.EmailField()
    mensagem = forms.CharField(widget=widgets.Textarea)

    def enviar_email(self):
        kwargs = {
            "subject": "Contato pelo site",
            "from_email": self.data["email"],
            "recipient_list": [settings.EMAIL_ADMIN],
            "message": self.data["mensagem"],
        }
        mail.send_mail(**kwargs)
