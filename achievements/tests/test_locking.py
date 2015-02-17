from django.test import TestCase
from accounts import mommy_recipes as accounts_recipes
from movies import mommy_recipes as movies_recipes
from achievements import mommy_recipes as achievements_recipes

class LockingTest(TestCase):

    def setUp(self):
        self.user = accounts_recipes.user.make()

    def test_delete_related_movie_achievements(self):
        movie = movies_recipes.movie.make()
        achievement = achievements_recipes.achievement.make(
            condition_movie=movie,
        )
        self.user.add_movie(movie)
        self.assertIn(achievement, self.user.get_achievements())
        self.user.remove_movie(movie)
        self.assertNotIn(achievement, self.user.get_achievements())

