from model_mommy.recipe import Recipe, foreign_key
from accounts.mommy_recipes import user
from movies.models import Movie, UserToMovie

movie = Recipe(
    Movie,
)

user_to_movie = Recipe(
    UserToMovie,
    user=foreign_key(user),
    movie=foreign_key(movie),
)
