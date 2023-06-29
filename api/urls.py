from django.urls import path

from api.views import BookReviewAPIView, BookReviewListAPIVIew

app_name = 'api'

urlpatterns = [
    path('reviews/', BookReviewListAPIVIew.as_view(), name='reviews-list'),
    path('review/<int:id>/', BookReviewAPIView.as_view(), name='review-detail')

]
