from django.shortcuts import render
from django.views.generic import ListView, DetailView
from typing import Optional, Union, Sequence
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

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
