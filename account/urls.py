from django.urls import path

from . import views
urlpatterns = [
      path('user-registration/', views.user_registration, name='user_registration'),
      path('user-login/', views.user_login, name='user_login'),
      path('user-logout/', views.user_logout, name='user_logout'),
      path('user-profile/', views.user_profile, name='user_profile'),
      path('user-picture/', views.user_picture, name='user_picture'),
      path('user-blogs/', views.user_blogs, name='user_blogs'),
      path('user-info/<str:username>/', views.user_info, name='user_info'),
      path('user-follow-or-unfollow/<int:id>/', views.user_follow_or_unfollow, name='user_follow_or_unfollow'),
      path('user-mute-or-unmute/<int:id>/', views.user_mute_or_unmute, name='user_mute_or_unmute'),
]
