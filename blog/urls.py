from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog-category/<str:slug>/', views.blog_category, name='blog_category'),
    path('blog-tag/<str:slug>/', views.blog_tag, name='blog_tag'),
    path('blog-details/<str:slug>/', views.blog_details, name='blog_details'),
    path('blog-comment/<str:slug>/', views.blog_comment, name='blog_comment'),
    path('blog-reply/<int:blog_id>/<int:comment_id>/', views.blog_reply, name='blog_reply'),
    path('blog-like/<int:pk>/', views.blog_like, name='blog_like'),
    path('blog-search/', views.blog_search, name='blog_search'),
    path('blog-add/', views.blog_add, name='blog_add'),
    path('blog-update/<str:slug>/', views.blog_update, name='blog_update'),
]