from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from message.models import Message

from django.contrib.auth.mixins import LoginRequiredMixin


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 3
    extra_context = {
        'title': 'Сообщения'
    }


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {
        'title': 'Сообщение'
    }


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('subject', 'text',)

    extra_context = {
        'title': 'Форма по добавлению'
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('message:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('subject', 'text',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message

    extra_context = {
        'title': 'Удаление сообщения'
    }
    success_url = reverse_lazy('message:message_list')
