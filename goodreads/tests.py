from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1', description="description1", isbn='123455243')
        user = CustomUser.objects.create(
            username='jama', first_name="Jamshid", last_name="Anorbekov", email="jama@mail.ru"
        )
        user.set_password("somepass")
        user.save()

        review1 = BookReview.objects.create(user=user, book=book, comment="Good book", stars_given=5)
        review2 = BookReview.objects.create(user=user, book=book, comment="Nice book", stars_given=4)
        review3 = BookReview.objects.create(user=user, book=book, comment="Not bad book", stars_given=3)

        response = self.client.get(reverse("home_page") + '?page_size=2')
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)

        self.assertNotContains(response, review1.comment)
