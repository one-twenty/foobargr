from .models import Category


def add_categories(request):
    return {'categories': Category.objects.all}
