from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import UpdateView, DetailView, DeleteView, CreateView, ListView

from Blog.blog_filter import PostFilter
from Blog.forms import UserCreateForm
from Blog.models import Post
# from django.db.models import Q





class PostList(generic.ListView):
    """

    ●	Display all posts along with their author name, posted date & thumbnail.
     ◦ Add search options to search blog by title and author.
    """
    # queryset = Post.objects.all()
    model = Post
    template_name = 'blog_post/Home.html'  # a list of all posts will be displayed on index.html
    context_object_name = 'post_list'

    # def get_queryset(self):
    #     post = super(PostList, self).get_queryset()
    #     query = self.request.GET.get('search')
    #     if query:
    #         postresult = Post.objects.filter(Q(title__icontains=query)
    #                                          | Q(title__in=query)
    #                                          | Q(author__in=query)
    #
    #                                          )
    #         post = postresult
    #     else:
    #         post = None
    #     return post
    # def get_queryset(self):
    #     qs = self.model.objects.all()
    #     filtered_model_list = PostFilter(self.request.GET, queryset=qs)
    #     return filtered_model_list.qs

    def get_context_data(self, **kwargs):
        context_data = super(PostList, self).get_context_data(**kwargs)
        f = PostFilter(self.request.GET, queryset=self.get_queryset())
        context_data['filter'] = f
        return context_data


class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog_post/post_detail.html'  # detail about each blog post will be on post_detail.html


# ====================

@method_decorator(login_required, name='dispatch')
class BlogListView(ListView):
    model = Post
    template_name = 'blog_post/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blog_post/post_form.html'
    success_url = reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'blog_post/post_confirm_delete.html'
    success_url = reverse_lazy('profile')


class BlogDetailView(DetailView):
    """
    AUTH: Any Anonymous users can read blogs.
    """
    model = Post
    template_name = 'blog_post/post_detail.html'
    success_url = reverse_lazy('profile')
    context_object_name = 'post'


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'blog_post/post_update.html'
    success_url = reverse_lazy('profile')
    context_object_name = 'post'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                name=form.cleaned_data['name'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


def About(request):
    return render(request, 'blog/about.html')
