from datetime import datetime

from django import forms

from .mixins import StyledFormMixin
from .models import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["first_mailing_date",
                  "frequency", "status", "message", "client", "owner"]

class MailingModeratorForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["message", "client", "owner"]