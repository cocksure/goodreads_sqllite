from django.urls import path
from books.views import BooksView, BookDetailView, AddReviewView, UpdateBookReviewView,\
    ConfirmDeleteReviewView, DeleteReviewView

app_name = 'books'

urlpatterns = [
    path("", BooksView.as_view(), name="list"),
    path("<int:id>/", BookDetailView.as_view(), name="detail"),
    path("<int:id>/reviews", AddReviewView.as_view(), name="reviews"),
    path("<int:book_id>/reviews/<int:review_id>/edit/", UpdateBookReviewView.as_view(), name="update-reviews"),
    path("<int:book_id>/reviews/<int:review_id>/confirm-delete/",
         ConfirmDeleteReviewView.as_view(), name="confirm-delete-review"),

    path("<int:book_id>/reviews/<int:review_id>/delete/", DeleteReviewView.as_view(), name="delete-review"),
]
