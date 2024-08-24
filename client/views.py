
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from client.models import Client


class ClientListView(ListView):
    model = Client
    paginate_by = 2
    extra_context = {
        'title': 'Клиенты'
    }


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Клиент'
    }


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment',)
    extra_context = {
        'title': 'Форма по добавлению'
    }

    def get_success_url(self):
        return reverse('client:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {
        'title': 'Удаление клиента'
    }
    success_url = reverse_lazy('client:client_list')

