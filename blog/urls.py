from django.urls import path
from .views import  (PostDetailView, PostCreateView, 
                    PostUpdateView, PostDeleteView
                    , SearchView)
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('post/new', PostCreateView.as_view(), name="post-create"),
    path('post/<str:slug>', PostDetailView.as_view(), name="blog-detail"),
    path('post/<str:slug>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('post/<str:slug>/update', PostUpdateView.as_view(), name="post-update"),
    path('search/', SearchView.as_view(template_name="blog/search.html"), name="search")
    
]