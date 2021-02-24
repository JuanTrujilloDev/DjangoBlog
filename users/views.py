from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Profile
from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
# Create your views here.

def register(request):

    if request.user.is_authenticated:
        return redirect('blog-home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}, now you can log-in!')
                return redirect('blog-home')

        else:
            
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def userProfile(request, slug):

    if request.user.is_authenticated:

        user = Profile.objects.get(slug = slug)
        posts = Post.objects.filter(author = user.user)
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'user': user, 'posts':page_obj}
        return render(request, 'users/profile.html', context)
    else:
        return redirect('login')

@login_required
def userProfileUpdate(request):
    
    if request.user.is_authenticated:

        if request.method== 'POST':
            user_form = UserUpdateForm(request.POST,instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect(request.user.profile.get_absolute_url())

        else:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form':user_form,
            'profile_form':profile_form
        }

        template_name = 'users/profileUpdate.html'

        return render(request, template_name, context)

    
    else:
        return redirect('login')


@login_required
def userDeleteView(request):
    if request.user.is_authenticated:
        obj = User.objects.get(username=request.user)
        if request.method == 'POST':
            obj.delete()
            return redirect('login')
        context = {'object':obj}
        template_name = "users/delete.html"

        return render(request, template_name, context)

    








