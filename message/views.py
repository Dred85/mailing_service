from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from message.models import Message

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения'
    }


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    extra_context = {
        'title': 'Сообщение'
    }
    permission_required = "mailing.settings_list"


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'text',)
    extra_context = {
        'title': 'Форма по добавлению'
    }
    permission_required = "mailing.settings_list"

    def get_success_url(self):
        return reverse('message:message_list')


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    fields = ('subject', 'text',)
    extra_context = {
        'title': 'Форма по редактированию'
    }
    permission_required = "mailing.message_list"

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = "mailing.message_list"
    extra_context = {
        'title': 'Удаление сообщения'
    }
    success_url = reverse_lazy('message:message_list')
