from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import Client


class HomeView(ListView):
    model = Client
    template_name = "client/home.html"


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 3
    extra_context = {"title": "Клиенты"}

    def get_object(self, queryset=None):
        return Client.objects.filter(
            owner=self.request.user
        ).first()  # Возвращаем сообщение текущего пользователя, если он есть, иначе None

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get(
            "sort", "email"
        )  # По умолчанию сортировка по email
        return queryset.order_by(sort_by)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {"title": "Клиент"}
    permission_required = "mailing.settings_list"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ("first_name", "last_name", "email", "comment")

    extra_context = {"title": "Форма по добавлению"}

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    # permission_required = "mailing.settings_list"

    def get_success_url(self):
        return reverse("client:client_list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client

    fields = ("first_name", "last_name", "email", "comment", "owner")
    extra_context = {"title": "Форма по редактированию"}

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("client:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client

    extra_context = {"title": "Удаление клиента"}
    success_url = reverse_lazy("client:client_list")
