# noinspection PyPackageRequirements
from model_mommy.recipe import Recipe
from movies.models import Movie, MovieChain

movie = Recipe(
    Movie,
)

movie_chain = Recipe(
    MovieChain,
)
