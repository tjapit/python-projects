from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from typing import (
    Optional, 
    Union, 
    Sequence,
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

    # pagination attribute, # posts/page
    paginate_by: int = 5

class UserPostListView(ListView):
    """ ListView for Posts by a specific User """
    model = Post
    template_name: str = 'blog/user_posts.html'
    context_object_name: Optional[str] = 'posts'
    paginate_by: int = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


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

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # template default naming for CreateView and UpdateView is <model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> Optional[bool]:
        """ Checks if the User passes a certain test. In this case, a User can only update a Post if they are the author of the Post """
        post = self.get_object()
        return True if self.request.user == post.author else False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url: Optional[str] = '/'

    def test_func(self) -> Optional[bool]:
        """ Checks if the User passes a certain test. In this case, a User can only delete a Post if they are the author of the Post """
        post = self.get_object()
        return True if self.request.user == post.author else False


def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
