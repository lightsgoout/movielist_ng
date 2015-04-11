# noinspection PyPackageRequirements
from model_mommy.recipe import Recipe
from movies.models import Movie, MovieChain, UserToMovie

movie = Recipe(
    Movie,
)

movie_chain = Recipe(
    MovieChain,
)

user_to_movie = Recipe(
    UserToMovie,
)
