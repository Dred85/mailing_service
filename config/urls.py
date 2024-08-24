from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from config import settings
from message.apps import MessageConfig

app_name = MessageConfig.name

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('client.urls', namespace='client')),
                  path('message/', include('message.urls', namespace='message')),
                  path('mailing/', include('mailing.urls', namespace='mailing')),
                  path('blog/', include('blog.urls', namespace='blog')),
                  path("users/", include("users.urls", namespace="users")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
