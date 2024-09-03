from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "views_count",
    )
    list_filter = (
        "title",
        "created_at",
        "views_count",
    )
    search_fields = (
        "title",
        "body",
    )
