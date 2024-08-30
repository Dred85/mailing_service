from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailing.forms import MailingModeratorForm, SettingsForm
from mailing.models import Settings
from django.core.exceptions import PermissionDenied


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


class SettingsUpdateView(LoginRequiredMixin,  UpdateView):
    model = Settings
    form_class = SettingsForm

    extra_context = {
        'title': 'Форма по редактированию'
    }


    def get_success_url(self):
        return reverse('mailing:settings_detail', args=[self.kwargs.get('pk')])


class SettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Settings
    form_class = SettingsForm


    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('mailing:settings_list')
