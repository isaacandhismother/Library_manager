from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from library.models import Book
from library.models import Category
from users.models import TakenBook
from users.models import WishlistBook
from users.models import ReturnedBook
from users.models import Notification

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from library.serializers import BookSerializer
from library.serializers import TakenBookSerializer
from library.serializers import WishlistBookSerializer


class BookListView(ListView):
    model = Book
    template_name = 'library/home.html'
    context_object_name = 'books'
    paginate_by = 44

    def get_queryset(self):
        queryset = Book.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(book_count=Count('book'))
        context['all_book_count'] = Book.objects.count()
        context['selected_category'] = self.request.GET.get('category')

        if self.request.user.is_authenticated:
            context['wishlist_books'] = WishlistBook.objects.filter(user=self.request.user).values_list('book_id', flat=True)
            notifications = Notification.objects.filter(user=self.request.user).order_by('-created_at')
            context['notifications'] = notifications
            context['unread_notifications'] = notifications.filter(read=False)

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['wishlist_books'] = WishlistBook.objects.filter(user=self.request.user).values_list('book_id', flat=True)

        return context


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def top_books(self, request):
        top_books = Book.objects.annotate(times_taken_count=Count('times_taken')).order_by('-times_taken_count')[:10]
        serializer = self.get_serializer(top_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sorted_books(self, request):
        sort_by = request.query_params.get('sort_by', 'title')
        books = Book.objects.all().order_by(sort_by)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class TakenBookViewSet(viewsets.ModelViewSet):
    queryset = TakenBook.objects.all()
    serializer_class = TakenBookSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        stats = {
            'total_books_returned': ReturnedBook.objects.count(),
            'books_awaiting': TakenBook.objects.filter(status='Awaiting').count(),
            'books_taken': TakenBook.objects.filter(status='Taken').count(),
        }
        return Response(stats)

    @action(detail=False, methods=['get'])
    def top_popular_books(self, request):
        popular_books = Book.objects.annotate(taken_count=Count('takenbook')).order_by('-taken_count')[:10]
        serializer = BookSerializer(popular_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_overdue_books(self, request):
        overdue_books = TakenBook.objects.filter(status='Taken', date_taken__lte=timezone.now() - timedelta(weeks=1)).order_by('-date_taken')[:100]
        serializer = self.get_serializer(overdue_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_users_with_overdue_books(self, request):
        top_users = TakenBook.objects.filter(status='Taken', date_taken__lte=timezone.now() - timedelta(weeks=1)).values('user').annotate(overdue_count=Count('id')).order_by('-overdue_count')[:100]
        return Response(top_users)


class WishlistBookViewSet(viewsets.ModelViewSet):
    queryset = WishlistBook.objects.all()
    serializer_class = WishlistBookSerializer


def search_results(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        results = Book.objects.filter(title__icontains=query)
    else:
        results = Book.objects.none()

    if category_id:
        results = results.filter(category__id=category_id)

    paginator = Paginator(results, 40)
    page_number = request.GET.get('page')

    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        'paginator': paginator,
        'results': results,
        'query': query,
        'category_id': category_id,
    }

    return render(request, 'library/search_results.html', context)
