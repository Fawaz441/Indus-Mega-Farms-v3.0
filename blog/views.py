from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView

class PostListView(ListView):
    model = Post
    template_name='blog/list.html'
    context_object_name = 'posts'
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    lookup_field = 'slug'