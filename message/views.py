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

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'subject')  # По умолчанию сортировка по имени
        return queryset.order_by(sort_by)


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

    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()  # Получаем стандартные аргументы формы
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:settings_list')  # Укажите URL для перенаправления после успешного создания


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
