from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from blog.models import Blog

from django.urls import reverse
from pytils.translit import slugify

from django.contrib.auth.mixins import LoginRequiredMixin


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = (
        "title",
        "content",
        "preview_image",
        "is_published",
        "views_count",
    )
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = (
        "title",
        "content",
        "preview_image",
        "is_published",
        "views_count",
    )

    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")
