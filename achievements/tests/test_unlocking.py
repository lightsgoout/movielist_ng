from django.test import TestCase
import freezegun
from accounts import mommy_recipes as accounts_recipes
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

    def test_condition_deadline(self):
        movie = movies_recipes.movie.make()
        achievement = achievements_recipes.achievement.make(
            condition_movie=movie,
            condition_deadline='2014-05-05'
        )
        with freezegun.freeze_time('2014-05-06'):
            u2m = movies_recipes.user_to_movie.make(
                user=self.user,
                movie=movie,
                status=UserToMovie.WATCHED,
            )
            self.assertNotIn(achievement, self.user.achievements.all())
            u2m.delete()

        with freezegun.freeze_time('2014-05-05'):
            u2m = movies_recipes.user_to_movie.make(
                user=self.user,
                movie=movie,
                status=UserToMovie.WATCHED,
            )
            self.assertIn(achievement, self.user.achievements.all())




