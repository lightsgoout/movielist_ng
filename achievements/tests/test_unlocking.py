from django.test import TestCase
from accounts import mommy_recipes as accounts_recipes
from accounts.models import MovielistUser
from movies import mommy_recipes as movies_recipes
from achievements import mommy_recipes as achievements_recipes
from movies.models import UserToMovie


class UnlockingTest(TestCase):

    def setUp(self):
        self.user = accounts_recipes.user.make()

    def test_condition_movie(self):
        movie = movies_recipes.movie.make()
        achievement = achievements_recipes.achievement.make(
            condition_movie=movie,
        )
        movies_recipes.user_to_movie.make(
            user=self.user,
            movie=movie,
            status=UserToMovie.WATCHED,
        )

        self.assertIn(achievement, self.user.achievements.all())





