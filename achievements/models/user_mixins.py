from django.db import models, transaction
from achievements import signals
from .relations import UserToAchievement


class UserAchievementsMixin(models.Model):
    class Meta:
        abstract = True

    achievements = models.ManyToManyField(
        'achievements.Achievement',
        through='achievements.UserToAchievement',
        related_name='users',
        blank=True,)

    def get_achievements(self, *args, **kwargs):
        return self.achievements.filter(
            *args,
            **kwargs
        )

    def add_achievement(self, achievement):
        """
        @type achievement achievements.models.Achievement
        """
        with transaction.atomic():
            u2m = UserToAchievement.objects.create(
                user=self,
                achievement=achievement,
            )
            signals.achievement_unlocked.send(
                sender=self.__class__,
                achievement=achievement,
                user=self,
            )
        return u2m

    def remove_achievement(self, achievement):
        with transaction.atomic():
            UserToAchievement.objects.filter(
                user=self,
                achievement=achievement
            ).delete()
            signals.achievement_locked.send(
                sender=self.__class__,
                achievement=achievement,
                user=self,
            )
