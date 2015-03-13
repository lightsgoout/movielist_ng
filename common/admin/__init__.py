from django.contrib import admin
from common import models
from common.admin.country import CountryAdmin

admin.site.register(models.Country, CountryAdmin)
