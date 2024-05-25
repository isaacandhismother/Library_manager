from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from library.models import Book
from users.forms import LoginUserForm, RegisterForm
from users.models import TakenBook
from users.models import WishlistBook
from users.models import Notification


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Register'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def taken_books_view(request):
    user = request.user
    taken_books = user.takenbook_set.all()
    has_taken_books = taken_books.exists()
    return render(request, 'users/taken_books.html', {'taken_books': taken_books,
                                                      'title': 'Taken books',
                                                      'has_taken_books': has_taken_books})


@login_required
def take_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('users/login')

    book = get_object_or_404(Book, id=book_id)

    if TakenBook.objects.filter(user=request.user, book=book).exists():
        return redirect('home')

    if book.stock > 0:
        TakenBook.objects.create(user=request.user, book=book, status='Awaiting')
        book.times_taken += 1
        book.save()

    return redirect('home')


@login_required
def wishlist_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    WishlistBook.objects.create(user=request.user, book=book)
    return redirect('home')


@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    WishlistBook.objects.filter(user=request.user, book=book).delete()
    return redirect('home')


@login_required
def wishlist_view(request):
    user = request.user
    wishlist_books = WishlistBook.objects.filter(user=request.user)
    return render(request, 'users/wishlist.html', context={'wishlist_books': wishlist_books, 'title': 'Wishlist'})


@require_POST
def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
