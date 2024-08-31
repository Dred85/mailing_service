from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from mailing.forms import SettingsForm, MailingModeratorForm
from mailing.models import Settings


class SettingsListView(LoginRequiredMixin, ListView):
    model = Settings
    paginate_by = 3
    extra_context = {
        'title': 'Рассылки'
    }


class SettingsDetailView(LoginRequiredMixin, DetailView):
    model = Settings
    permission_required = "mailing.settings_list"
    extra_context = {
        'title': 'Рассылка'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object  # объект Settings
        return context


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


class SettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Settings


    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return SettingsForm
        if (
                user.has_perm("mailing.can_disabled_mailing")
        ):
            return MailingModeratorForm
        raise PermissionDenied

    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('mailing:settings_list')


class SettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Settings
    form_class = SettingsForm

    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('mailing:settings_list')
