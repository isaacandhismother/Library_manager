from django.contrib import admin

from library.models import Book
from library.models import Author
from library.models import Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class BookCategoryInline(admin.TabularInline):
    model = Book.category.through
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'stock', 'times_taken']
    list_filter = ['author', 'category', 'stock']
    search_fields = ['title', 'author', 'category']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookCategoryInline]
    list_display = ['name']
    search_fields = ['name']
