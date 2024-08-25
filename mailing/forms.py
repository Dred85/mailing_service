from datetime import datetime

from django import forms

from .mixins import StyledFormMixin
from .models import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["first_mailing_date",
                  "frequency", "status", "message", "client", "owner",  "is_active"]

class MailingModeratorForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["is_active"]