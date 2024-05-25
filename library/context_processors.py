from django.db.models import Count
from library.models import Category, Book


def categories_processor(request):
    categories = Category.objects.annotate(book_count=Count('book'))
    all_book_count = Book.objects.count()
    return {'categories': categories, 'all_book_count': all_book_count}
