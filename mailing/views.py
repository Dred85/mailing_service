from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from mailing.cron import send_mailing_email
from mailing.forms import SettingsForm, MailingModeratorForm, MailingModeratorFormOwner
from mailing.models import Settings, Attempt


class SettingsListView(LoginRequiredMixin, ListView):
    model = Settings
    paginate_by = 3
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'client')  # По умолчанию сортировка по имени
        return queryset.order_by(sort_by)


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
    form_class = MailingModeratorFormOwner
    extra_context = {
        'title': 'Форма по добавлению'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()  # Получаю стандартные аргументы формы
        kwargs['user'] = self.request.user  # Передаю текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаю владельца


        mailing_item = form.save()  # Сначала сохраняю объект Settings

        # После этого отправляю письма
        selected_clients = form.cleaned_data['client']  # Получаю выбранных клиентов
        send_mailing_email(mailing_item, selected_clients)  # Отправляю сообщения только выбранным клиентам

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

    extra_context = {
        'title': 'Удаление рассылки'
    }

    success_url = reverse_lazy('mailing:settings_list')


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    paginate_by = 3
    extra_context = {
        'title': 'Отчет о попытках'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'mailing')  # По умолчанию сортировка по имени
        return queryset.order_by(sort_by)
