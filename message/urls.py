from django.urls import path

from message.apps import MessageConfig
from message.views import MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView
from django.views.decorators.cache import never_cache

app_name = MessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('update/<int:pk>/', never_cache(MessageUpdateView.as_view()), name='message_update'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('create/', never_cache(MessageCreateView.as_view()), name='message_create'),
]