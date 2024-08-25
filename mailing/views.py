from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailing.forms import MailingModeratorForm, SettingsForm
from mailing.models import Settings
from django.core.exceptions import PermissionDenied

class SettingsListView(LoginRequiredMixin, ListView):
    model = Settings
    extra_context = {
        'title': 'Рассылки'
    }


class SettingsDetailView(LoginRequiredMixin, DetailView):
    model = Settings
    permission_required = "mailing.settings_list"
    extra_context = {
        'title': 'Рассылка'
    }


class SettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Settings
    fields = ('first_mailing_date', 'frequency', 'status', 'message', 'client',)
    extra_context = {
        'title': 'Форма по добавлению'
    }
    permission_required = "mailing.message_list"

    def get_success_url(self):
        return reverse('mailing:settings_list')


class SettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Settings
    permission_required = "mailing.message_list"
    fields = ('first_mailing_date', 'frequency', 'status', 'message', 'client',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return SettingsForm
        if user.has_perm("can_view_mailing") and user.has_perm("can_view_users") and user.has_perm(
                "can_blocked_users") and user.has_perm("can_disabled_mailing"):
            return MailingModeratorForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse('mailing:settings_detail', args=[self.kwargs.get('pk')])


class SettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Settings
    permission_required = "mailing.message_list"

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return SettingsForm
        if user.has_perm("can_view_mailing") and user.has_perm("can_view_users") and user.has_perm(
                "can_blocked_users") and user.has_perm("can_disabled_mailing"):
            return MailingModeratorForm
        raise PermissionDenied

    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('mailing:settings_list')
