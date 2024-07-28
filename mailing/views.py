
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailing.models import Settings


class SettingsListView(ListView):
    model = Settings
    extra_context = {
        'title': 'Рассылки'
    }


class SettingsDetailView(DetailView):
    model = Settings
    extra_context = {
        'title': 'Рассылка'
    }


class SettingsCreateView(CreateView):
    model = Settings
    fields = ('first_mailing_date', 'frequency', 'status', 'message', 'client',)
    extra_context = {
        'title': 'Форма по добавлению'
    }

    def get_success_url(self):
        return reverse('mailing:settings_list')


class SettingsUpdateView(UpdateView):
    model = Settings
    fields = ('first_mailing_date', 'frequency', 'status', 'message', 'client',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('mailing:settings_detail', args=[self.kwargs.get('pk')])


class SettingsDeleteView(DeleteView):
    model = Settings
    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('mailing:settings_list')

