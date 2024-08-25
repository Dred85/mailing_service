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


class SettingsCreateView(LoginRequiredMixin, CreateView):
    model = Settings
    form_class = SettingsForm

    extra_context = {
        'title': 'Форма по добавлению'
    }


    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:settings_list')


class SettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Settings
    form_class = SettingsForm

    permission_required = (
        "mailing.can_view_mailing",
        "mailing.can_view_users",
        "mailing.can_blocked_users",
        "mailing.can_disabled_mailing",
    )
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
    form_class = SettingsForm

    permission_required = (
        "mailing.can_view_mailing",
        "mailing.can_view_users",
        "mailing.can_blocked_users",
        "mailing.can_disabled_mailing",
    )

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
