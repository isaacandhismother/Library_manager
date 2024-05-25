from django.db import models


class Author(models.Model):
    name = models.CharField('Name', max_length=63)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=63)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('Title', max_length=63)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category, blank=False)
    cover = models.ImageField(upload_to='media/', blank=True)
    stock = models.IntegerField(default=0)
    times_taken = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
