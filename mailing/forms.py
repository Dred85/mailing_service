from django import forms

from client.models import Client
from .mixins import StyledFormMixin
from .models import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        user = forms.ChoiceField(required=True)
        fields = ["first_mailing_date",
                  "frequency", "status", "message", "client", "owner", "is_active"]


class MailingModeratorForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["is_active"]


class MailingModeratorFormOwner(StyledFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из аргументов
        super(MailingModeratorFormOwner, self).__init__(*args, **kwargs)

        if user:
            # Фильтруем клиентов по текущему пользователю
            self.fields['client'].queryset = Client.objects.filter(owner=user)
            self.fields['message'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Settings
        fields = '__all__'  # Используйте '__all__', чтобы указать все поля

