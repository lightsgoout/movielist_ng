from accounts.models import MovielistUser


class EmailBackend(object):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = MovielistUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except MovielistUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return MovielistUser.objects.get(pk=user_id)
        except MovielistUser.DoesNotExist:
            return None
