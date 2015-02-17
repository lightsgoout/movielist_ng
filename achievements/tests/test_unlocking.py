from django.test import TestCase
import freezegun
from accounts import mommy_recipes as accounts_recipes
from movies import mommy_recipes as movies_recipes
from achievements import mommy_recipes as achievements_recipes


class UnlockingTest(TestCase):

    def setUp(self):
        self.user = accounts_recipes.user.make()

    def test_condition_deadline(self):
        movie = movies_recipes.movie.make()
        achievement = achievements_recipes.achievement.make(
            condition_movie=movie,
            condition_deadline='2014-05-05'
        )
        with freezegun.freeze_time('2014-05-06'):
            self.user.add_movie(movie)
            self.assertNotIn(achievement, self.user.get_achievements())
            self.user.remove_movie(movie)

        with freezegun.freeze_time('2014-05-05'):
            self.user.add_movie(movie)
            self.assertIn(achievement, self.user.get_achievements())

    def test_condition_movie(self):
        movie = movies_recipes.movie.make()
        achievement = achievements_recipes.achievement.make(
            condition_movie=movie,
        )
        self.user.add_movie(movie)

        self.assertIn(achievement, self.user.get_achievements())

    def test_condition_movie_year(self):
        movie = movies_recipes.movie.make(year=2007)
        achievement = achievements_recipes.achievement.make(
            condition_movie_year=2006,
        )

        self.user.add_movie(movie)
        self.assertNotIn(achievement, self.user.get_achievements())

        self.user.remove_movie(movie)
        achievement.condition_movie_year = 2007
        achievement.save(update_fields=('condition_movie_year',))

        self.user.add_movie(movie)
        self.assertIn(achievement, self.user.get_achievements())

    def test_condition_movie_year_multiple_ties(self):
        movies = movies_recipes.movie.make(year=2007, _quantity=5)
        achievement = achievements_recipes.achievement.make(
            condition_movie_year=2007,
            condition_times=5,
        )

        for movie in movies[:4]:
            self.user.add_movie(movie)

        self.assertNotIn(achievement, self.user.get_achievements())
        self.user.add_movie(movies[-1])
        self.assertIn(achievement, self.user.get_achievements())

    def test_condition_movie_rated(self):
        movie = movies_recipes.movie.make(rated='R')
        achievement = achievements_recipes.achievement.make(
            condition_movie_rated='PG-13',
        )

        self.user.add_movie(movie)
        self.assertNotIn(achievement, self.user.get_achievements())

        self.user.remove_movie(movie)
        achievement.condition_movie_rated = 'R'
        achievement.save(update_fields=('condition_movie_rated',))

        self.user.add_movie(movie)
        self.assertIn(achievement, self.user.get_achievements())

    def test_condition_movie_rated_multiple_ties(self):
        movies = movies_recipes.movie.make(rated='R', _quantity=5)
        achievement = achievements_recipes.achievement.make(
            condition_movie_rated='R',
            condition_times=5,
        )

        for movie in movies[:4]:
            self.user.add_movie(movie)

        self.assertNotIn(achievement, self.user.get_achievements())
        self.user.add_movie(movies[-1])
        self.assertIn(achievement, self.user.get_achievements())
