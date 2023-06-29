from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):

    if created:
        send_mail(
            "Welcome to goodreads clone site",
            f"Hi, {instance.username}. Welcome to Goodreads Clone. Enjoy the books and reviews",
            "AdaptaMail@gmail.com",
            [instance.email]
        )
