from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from library.views import BookListView
from library.views import BookDetailView
from library.views import search_results

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('search/', search_results, name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
