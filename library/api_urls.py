from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, TakenBookViewSet, WishlistBookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'takenbooks', TakenBookViewSet)
router.register(r'wishlistbooks', WishlistBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
