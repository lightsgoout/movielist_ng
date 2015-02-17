from django.db import models
from .relations import UserToAchievement


class UserAchievementsMixin(models.Model):
    class Meta:
        abstract = True

    achievements = models.ManyToManyField(
        'achievements.Achievement',
        through='achievements.UserToAchievement',
        related_name='users',
        blank=True,)

    def get_achievements(self, is_locked=False, **kwargs):
        return self.achievements.filter(
            usertoachievement__is_locked=is_locked,
            **kwargs
        )

    def add_achievement(self, achievement, is_locked=False):
        """
        @type achievement achievements.models.Achievement
        @type is_locked bool
        """
        return UserToAchievement.objects.create(
            user=self,
            achievement=achievement,
            is_locked=is_locked,
        )
