from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('category/<str:slug>/', views.category_blogs, name='category_blogs'),
    path('tag/<str:slug>/', views.tag_blogs, name='tag_blogs'),
    path('blog/<str:slug>/', views.blog_details, name='blog_details'),
    path('comment/<str:slug>/', views.add_comment, name='add_comment'),
    path('reply/<int:blog_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('like/<int:pk>/', views.blog_like, name='blog_like'),
]