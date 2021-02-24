from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, 
                                    CreateView, 
                                    UpdateView,
                                    DeleteView,
                                    ListView)
from django.core.paginator import Paginator
from .models import Post
from users.models import Profile
from django.db.models import Q

@login_required
def home(request):
    if request.user.is_authenticated:

        qs = Post.objects.order_by('-date_posted')
        post_count = Post.countPosts()
        user_count = Profile.countUsers()

        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
                'post_count': post_count,
                'user_count': user_count,
                'posts' : paginator.get_page(page_number),
            }
        template_name = "blog/home.html"
        return render(request, template_name, context)
    else: 

        return redirect('login')


def about(request):
    title = "About"
    template_name = "blog/about.html"
    context = {'title':title}
    return render(request, template_name, context)





@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'




@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/update.html"

    def form_valid(self, form):


        form.instance.author = self.request.user


        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if obj.author != self.request.user:
            return False
        return True

@method_decorator(login_required, name='dispatch')
class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = '/'

    def test_func(self):
        obj = self.get_object()
        
        if obj.author != self.request.user:
            return False
        return True

    '''ANOTHER WAY TO VALIDATE AUTHOR 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseForbidden()
        return super(EditPost, self).dispatch(request, *args, **kwargs)'''


@method_decorator(login_required, name='dispatch')
class SearchView(ListView):
    model = Post
    template_name = "blog/search.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        )
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')

        return context









