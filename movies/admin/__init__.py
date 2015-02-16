from django.contrib import admin
from movies import models
from movies.admin.movie.admin import MovieAdmin
from movies.admin.movie_chain import MovieChainAdmin

admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Person)
admin.site.register(models.MovieChain, MovieChainAdmin)
