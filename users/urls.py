from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.views import RegisterView
from users.views import taken_books_view
from users.views import take_book

from users.views import wishlist_book, remove_from_wishlist, wishlist_view
from users.views import mark_notifications_as_read

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('taken_books/', taken_books_view, name='taken_books'),
    path('take_book/<int:book_id>/', take_book, name='take_book'),
    path('wishlist_book/<int:book_id>/', wishlist_book, name='wishlist_book'),
    path('remove_from_woshlist/<int:book_id>', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist_books', wishlist_view, name='wishlist_books'),
    path('mark_notifications_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),
]
