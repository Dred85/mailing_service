from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from message.models import Message


class MessageListView(ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения'
    }


class MessageDetailView(DetailView):
    model = Message
    extra_context = {
        'title': 'Сообщение'
    }


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'text',)
    extra_context = {
        'title': 'Форма по добавлению'
    }

    def get_success_url(self):
        return reverse('message:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'text',)
    extra_context = {
        'title': 'Форма по редактированию'
    }

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    extra_context = {
        'title': 'Удаление сообщения'
    }
    success_url = reverse_lazy('message:message_list')