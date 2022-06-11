from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView
)
from typing import (
    Optional, 
    Union, 
    Sequence
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    """ Class-based view: List, Detail, Create, Update, Delete """
    # base model for class
    model = Post

    # default template naming scheme for class-based templates
    template_name: str = 'blog/home.html' # <app>/<model>_<viewtype>.html

    # default context name: object_list, change variable name to 'posts' because template already created
    context_object_name: Optional[str] = 'posts'

    # ordering Posts by most recently posted ('-' indicates reversed order)
    ordering: Optional[Union[str, Sequence[str]]] =  '-date_posted'

class PostDetailView(DetailView):
    """ Class-based view following Django's convention """
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # template default naming for CreateView and UpdateView is <model>_form.html

    def form_valid(self, form):
        # setting the author of the form (Post) as the current user logged in
        form.instance.author = self.request.user
        # before passing it to the form valid checker 
        return super().form_valid(form)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
