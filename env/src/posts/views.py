import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from .models import Post
from .forms import PostForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

class PostCreateView(StaffMemberRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

class PostDetailView(MemberRequiredMixin, DetailView):
    queryset = Post.objects.all()

    

class PostListView(ListView):
    def get_queryset(self):   
        request = self.request
        qs = Post.objects.all()
        query = request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs
"""
    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['random_integer'] = random.randint(100,1000)
        print(context)
        return context
"""
class PostUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Post.objects.all()
    form_class = PostForm

class PostDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    success_url = '/posts'
