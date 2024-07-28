from django.urls import path

from message.apps import MessageConfig
from message.views import MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView

app_name = MessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
]