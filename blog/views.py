from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.db.models import Q

from .models import Category, Tag, Blog, Comment, Reply
from .forms import TextForm


def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    context = {
        'blogs' : blogs,
        'tags' : tags,
    }
    return render(request, 'home.html', context)

def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    context = {
        'blogs' : blogs,
        'tags' : tags,
        'paginator' : paginator
    }
    return render(request, 'blogs.html', context)

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    context = {
        'blogs' : blogs,
        'tags' : tags,
        'all_blogs' : all_blogs
    }
    return render(request, 'category_blogs.html', context)

def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all()
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    context = {
        'blogs' : blogs,
        'tags' : tags,
        'all_blogs' : all_blogs
    }
    return render(request, 'tag_blogs.html', context)

def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    comments = blog.blog_comments.all()
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('created_date')
    liked_by = request.user in blog.likes.all()
    context = {
        'blog' : blog,
        'comments' : comments,
        'related_blogs' : related_blogs,
        'tags' : tags,
        'liked_by' : liked_by
    }
    return render(request, 'blog-details.html', context)

def add_comment(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data.get('text')
            )
            return redirect('blog_details', slug=slug)
        
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog_details', slug=blog.slug)

def blog_like(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {}
    
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count() 
    else:
        blog.likes.add(request.user)
        context['liked'] = True 
        context['like_count'] = blog.likes.all().count()
    return JsonResponse(context, safe=False)  

def blog_search(request):
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.order_by('created_date')
    tags = Tag.objects.order_by('-created_date')
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key)|
            Q(category__title__icontains=search_key)|
            Q(user__username__icontains=search_key)|
            Q(tags__title__icontains=search_key)
        ).distinct()
        context = {
            'blogs' : blogs,
            'recent_blogs' : recent_blogs,
            'tags' : tags,
            'search_key' : search_key
        }
        return render(request, 'search.html', context)
    else:
        return redirect('home')
    