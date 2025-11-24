from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Blogpost


class BlogHome(ListView):
    model = Blogpost
    context_object_name = "blog"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(published_on=True)


@method_decorator(login_required, name='dispatch')
class BlogPostCreate(CreateView):
    model = Blogpost
    template_name = "blog/blogpost_create.html"
    fields = ['title', 'content', ]


class BlogPostUpdate(UpdateView):
    model = Blogpost
    template_name = "blog/blogpost_edit.html"
    fields = ['title', 'content', 'published_on', ]


class BlogPostDetail(DetailView):
    model = Blogpost
    context_object_name = "post"


class BlogPostDelete(DeleteView):
    model = Blogpost
    context_object_name = "post"
    success_url = reverse_lazy("blog:home")
