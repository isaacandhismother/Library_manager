from rest_framework import serializers
from library.models import Book
from users.models import TakenBook, WishlistBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class TakenBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenBook
        fields = '__all__'


class WishlistBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistBook
        fields = '__all__'
