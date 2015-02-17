from django.contrib import admin

# Register your models here.
from achievements.forms import AchievementForm
from achievements.models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    form = AchievementForm


admin.site.register(Achievement, AchievementAdmin)
