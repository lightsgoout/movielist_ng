from django.db import models


class UserToAchievement(models.Model):
    user = models.ForeignKey('accounts.MovielistUser')
    achievement = models.ForeignKey('achievements.Achievement')
    unlocked_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        app_label = 'achievements'
