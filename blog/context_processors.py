from .models import Category, Tag

def get_all_categories(request):
    categories = Category.objects.order_by('-created_date')
    context = {
        'categories' : categories
    }
    return context

def get_all_tags(request):
    tags = Tag.objects.order_by('-created_date')
    context = {
        'tags' : tags
    }
    return context