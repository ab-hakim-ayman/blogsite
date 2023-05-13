from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('category_blogs/<str:slug>/', views.category_blogs, name='category_blogs'),
    path('tag_blogs/<str:slug>/', views.tag_blogs, name='tag_blogs'),
    path('blog/<str:slug>/', views.blog_details, name='blog_details'),
]