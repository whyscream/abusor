from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

User = get_user_model()


class Command(BaseCommand):
    help = "Create an authorization token for an API client."

    def add_arguments(self, parser):
        """Request the username variable."""
        parser.add_argument('username', type=str)

    def handle(self, *args, **kwargs):
        """Find the user and create a token."""
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError("User '{}' does not exist".format(username))

        try:
            token = Token.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS('Created token for user {}: {}'.format(username, token.key)))
        except IntegrityError:
            token = Token.objects.get(user=user)
            self.stdout.write(self.style.SUCCESS('Found existing token for user {}: {}'.format(username, token.key)))
