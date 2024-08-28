from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    BlogCreateView,
    BlogListView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)

app_name = BlogConfig.name
from django.views.decorators.cache import never_cache, cache_page

urlpatterns = [
    path("create", BlogCreateView.as_view(), name="create"),
    path("", cache_page(60)(BlogListView.as_view()), name="blog_list"),
    path("view/<int:pk>/", BlogDetailView.as_view(), name="view"),
    path("edit/<int:pk>/", BlogUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="delete"),
]
