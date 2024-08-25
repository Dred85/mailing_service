from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from client.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 2
    extra_context = {
        'title': 'Клиенты'
    }


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Клиент'
    }
    permission_required = "mailing.settings_list"


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment',)
    extra_context = {
        'title': 'Форма по добавлению'
    }
    permission_required = "mailing.settings_list"


    def get_success_url(self):
        return reverse('client:client_list')


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    permission_required = "mailing.settings_list"
    fields = ('first_name', 'last_name', 'email', 'comment',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = "mailing.settings_list"
    extra_context = {
        'title': 'Удаление клиента'
    }
    success_url = reverse_lazy('client:client_list')
