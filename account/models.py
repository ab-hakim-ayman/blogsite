from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email, **extra_fields):
        if not username:
            raise ValueError("username must be set!")
        if not password:
            raise ValueError("password must be set!")
        if not email:
            raise ValueError("email must be set!")
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            password = password,
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_stuff") is not True:
            raise ValueError("The superuser must have is_stuff = True!")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("The superuser must have is_superuser = True!")
        if extra_fields.get("is_active") is not True:
            raise ValueError("The superuser must have is_active = True!")
        return self.create_user(username, password, email, **extra_fields)
    
    
class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True, error_messages={
        "unique":"Email must be unique"
    })
    image = models.ImageField(null=True, blank=True, upload_to="user-images")
    followers = models.ManyToManyField("Follow")
    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def get_profile_picture(self):
        url = ""
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    followed_by = models.ForeignKey(
        User,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.followed_by.username} started following {self.followed.username}!"