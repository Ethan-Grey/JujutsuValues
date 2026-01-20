from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Creates the "Value Reviewers" group if it does not exist'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Value Reviewers")
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Value Reviewers" group')
            )
        else:
            self.stdout.write(
                self.style.WARNING('"Value Reviewers" group already exists')
            )
