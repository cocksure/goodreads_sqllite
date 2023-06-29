from django.contrib import admin
from .models import Book, BookAuthor, BookReview, Author


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('id', 'title', 'isbn', 'description')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')
    list_display = ('id', 'book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('user', 'book')
    list_display = ('id', 'user', 'book', 'stars_given')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)