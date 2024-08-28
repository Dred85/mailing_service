from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import SettingsListView, SettingsDetailView, SettingsUpdateView, SettingsDeleteView, \
    SettingsCreateView
from django.views.decorators.cache import never_cache, cache_page

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(SettingsListView.as_view()), name='settings_list'),
    path('<int:pk>/', SettingsDetailView.as_view(), name='settings_detail'),
    path('update/<int:pk>/', never_cache(SettingsUpdateView.as_view()), name='settings_update'),
    path('delete/<int:pk>/', SettingsDeleteView.as_view(), name='settings_delete'),
    path('create/', never_cache(SettingsCreateView.as_view()), name='settings_create'),
]