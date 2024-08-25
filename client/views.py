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


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Клиент'
    }
    permission_required = "mailing.settings_list"


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'email', 'comment', 'owner')

    permission_required = (
        "mailing.can_view_mailing",
        "mailing.can_view_users",
        "mailing.can_blocked_users",
        "mailing.can_disabled_mailing",
    )

    extra_context = {
        'title': 'Форма по добавлению'
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    # permission_required = "mailing.settings_list"

    def get_success_url(self):
        return reverse('client:client_list')


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client

    permission_required = (
        "mailing.can_view_mailing",
        "mailing.can_view_users",
        "mailing.can_blocked_users",
        "mailing.can_disabled_mailing",
    )
    fields = ('first_name', 'last_name', 'email', 'comment', 'owner')
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client

    permission_required = (
        "mailing.can_view_mailing",
        "mailing.can_view_users",
        "mailing.can_blocked_users",
        "mailing.can_disabled_mailing",
    )
    extra_context = {
        'title': 'Удаление клиента'
    }
    success_url = reverse_lazy('client:client_list')
