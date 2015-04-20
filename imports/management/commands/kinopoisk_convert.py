from django.core.management import BaseCommand
from django.db import transaction
from accounts.models import MovielistUser
from imports.kinopoisk_convert import convert


class Command(BaseCommand):

    def handle(self, *args, **options):
        with transaction.atomic():
            convert(MovielistUser.objects.get(username="shtaket"), "2589131")
            transaction.rollback()
