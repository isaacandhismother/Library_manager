from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import models, transaction
from django.urls import reverse

from library.models import Book


class User(AbstractUser):
    taken_books = models.ManyToManyField(Book, through='TakenBook', related_name='users')


class TakenBook(models.Model):
    STATUS_CHOICES = [
        ('Awaiting', 'Awaiting'),
        ('Taken', 'Taken'),
        ('Returned', 'Returned')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='Awaiting')

    def __str__(self):
        return f"{self.user.username} booked {self.book.title} on {self.date_taken}"

    class Meta:
        verbose_name = 'Taken Book'
        verbose_name_plural = 'Taken Books'


class ReturnedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_taken = models.DateTimeField()
    date_returned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} returned {self.book.title} on {self.date_returned}"

    class Meta:
        verbose_name = 'Returned Book'
        verbose_name_plural = 'Returned Books'


class WishlistBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} wishlisted {self.book.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=127)
    link = models.URLField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


@receiver(post_save, sender=TakenBook)
def decrease_book_stock(sender, instance, created, **kwargs):
    if created:
        instance.book.stock -= 1
        instance.book.save()


@receiver(pre_save, sender=TakenBook)
def create_returned_book(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = TakenBook.objects.get(pk=instance.pk)
        if previous_instance.status != 'Returned' and instance.status == 'Returned':

            def delete_and_create_returned_book():
                ReturnedBook.objects.create(
                    user=instance.user,
                    book=instance.book,
                    date_taken=instance.date_taken
                )
                instance.delete()

            transaction.on_commit(delete_and_create_returned_book)


@receiver(post_delete, sender=TakenBook)
def increase_book_stock(sender, instance, **kwargs):
    instance.book.stock += 1
    instance.book.save()
    notify_wishlist_users()


def notify_wishlist_users():
    books_in_stock = Book.objects.filter(stock__gt=0)
    for book in books_in_stock:
        wishlist_books = WishlistBook.objects.filter(book=book)
        for wishlist_book in wishlist_books:
            user = wishlist_book.user
            message = f'The book "{book.title}" is now in stock!'
            link = reverse('book_detail', args=[book.id])
            Notification.objects.create(user=user, message=message, link=link)


@receiver(post_save, sender=TakenBook)
def delete_wishlisted_book(sender, instance, created, **kwargs):
    if created:
        wishlisted_book = WishlistBook.objects.filter(user=instance.user, book=instance.book).first()
        if wishlisted_book:
            wishlisted_book.delete()
