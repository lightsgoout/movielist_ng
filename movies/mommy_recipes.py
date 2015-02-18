# noinspection PyPackageRequirements
from model_mommy.recipe import Recipe
from movies.models import Movie

movie = Recipe(
    Movie,
)
