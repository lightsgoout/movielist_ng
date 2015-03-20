from django.contrib import admin
from movies import models
from movies.admin.genre import GenreAdmin
from movies.admin.movie.admin import MovieAdmin
from movies.admin.movie_chain import MovieChainAdmin
from movies.admin.person.admin import PersonAdmin

admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.MovieChain, MovieChainAdmin)
