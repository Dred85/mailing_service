from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import SettingsListView, SettingsDetailView, SettingsUpdateView, SettingsDeleteView, \
    SettingsCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', SettingsListView.as_view(), name='settings_list'),
    path('<int:pk>/', SettingsDetailView.as_view(), name='settings_detail'),
    path('update/<int:pk>/', SettingsUpdateView.as_view(), name='settings_update'),
    path('delete/<int:pk>/', SettingsDeleteView.as_view(), name='settings_delete'),
    path('create/', SettingsCreateView.as_view(), name='settings_create'),
]