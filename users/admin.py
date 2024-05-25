from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, TakenBook, WishlistBook, ReturnedBook, Notification


class TakenBookInline(admin.TabularInline):
    model = TakenBook
    fields = ['book', 'date_taken', 'status']
    readonly_fields = ['date_taken']
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [TakenBookInline]


class TakenBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'date_taken', 'status')
    list_filter = ('status',)
    readonly_fields = ['date_taken']


class WishlistBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'date_added')
    search_fields = ('user__username', 'book__title')
    list_filter = ('date_added',)


class ReturnedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'date_taken', 'date_returned')
    search_fields = ('user__username', 'book__title')
    list_filter = ('date_taken', 'date_returned',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'link', 'created_at')
    search_fields = ('user',)
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(TakenBook, TakenBookAdmin)
admin.site.register(WishlistBook, WishlistBookAdmin)
admin.site.register(ReturnedBook, ReturnedBookAdmin)
admin.site.register(Notification, NotificationAdmin)
