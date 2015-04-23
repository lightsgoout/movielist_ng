from datetime import date
from django.core import validators
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from accounts import signals
from achievements.models.user_mixins import UserAchievementsMixin
from movies.models.user_mixins import UserMoviesMixin


class MovielistUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# noinspection PyMethodMayBeStatic
class MovielistUser(AbstractBaseUser, UserMoviesMixin, UserAchievementsMixin):
    username = models.CharField(
        'username',
        max_length=30,
        unique=True,
        help_text='Required. 30 characters or fewer. Letters, digits and '
                  '@/./+/-/_ only.',
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid'
            )
        ],
        db_index=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    country = models.ForeignKey('common.Country', null=True, blank=True)

    GENDER_MALE = True
    GENDER_FEMALE = False
    gender = models.NullBooleanField(default=None)

    objects = MovielistUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False
    )

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    # noinspection PyUnusedLocal
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def is_following(self, user):
        """
        @type user MovielistUser
        """
        return self.friends.filter(id=user.id).exists()

    def follow_user(self, user):
        """
        @type user MovielistUser
        """
        if not self.is_following(user):
            self.friends.add(user)
            signals.user_followed.send(
                sender=self.__class__,
                user=self,
                friend=user)

    def unfollow_user(self, user):
        """
        @type user MovielistUser
        """
        if self.is_following(user):
            self.friends.remove(user)
            signals.user_unfollowed.send(
                sender=self.__class__,
                user=self,
                friend=user)

    def get_followers(self):
        return MovielistUser.objects.filter(
            friends=self
        ).select_related(
            'last_watched_movie',
        ).order_by('id')

    def get_following(self):
        return self.friends.all(
        ).select_related(
            'last_watched_movie'
        ).order_by('id')
