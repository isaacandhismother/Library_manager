import random
from django.core.management.base import BaseCommand
from faker import Faker
from library.models import Book, Category, Author


class Command(BaseCommand):
    help = 'Generate random authors, categories, and books'

    def handle(self, *args, **kwargs):
        faker = Faker()

        category_names = ['Fiction', 'Science', 'History', 'Philosophy', 'Adventure', 'Biography', 'Fantasy', 'Mystery', 'Thriller', 'Romance']
        categories = [Category.objects.get_or_create(name=name)[0] for name in category_names]

        authors = [Author.objects.create(name=faker.name()) for _ in range(100)]

        for _ in range(1000):
            title = faker.sentence(nb_words=4)
            author = random.choice(authors)
            stock = random.randint(1, 100)
            times_taken = random.randint(0, 50)

            book = Book.objects.create(
                title=title,
                author=author,
                stock=stock,
                times_taken=times_taken
            )

            book.category.set(random.sample(categories, k=random.randint(1, 3)))
            book.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated 1000 books, 100 authors, and 10 categories'))
