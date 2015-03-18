from django.test import TestCase
from accounts import mommy_recipes as accounts_recipes
from movies import mommy_recipes as movie_recipes
from suggestions import factors
from suggestions.imdb import IMDBSuggester


class Test(TestCase):

    def setUp(self):
        self.user = accounts_recipes.user.make()
        self.suggester = IMDBSuggester()

    def test_suggest_by_top_imdb_order(self):
        movie0 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=9,
        )
        movie1 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=8
        )
        movie2 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=7,
        )
        movie3 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=6.9,
        )

        self.assertEqual(self.suggester.next_in_top(movie0), movie1)
        self.assertEqual(self.suggester.next_in_top(movie1), movie2)
        self.assertEqual(self.suggester.next_in_top(movie2), movie3)

    def test_get_suggestion_list_imdb_top(self):
        movie0 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=9,
        )
        movie1 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=8
        )
        movie2 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=7,
        )
        movie3 = movie_recipes.movie.make(
            votes_imdb=1000,
            rating_imdb=6.9,
        )
        self.assertEqual(self.suggester.get_suggestion_list(self.user), [
            (movie0, factors.FACTOR_IMDB_TOP),
            (movie1, factors.FACTOR_IMDB_TOP),
            (movie2, factors.FACTOR_IMDB_TOP),
            (movie3, factors.FACTOR_IMDB_TOP),
        ])

        self.assertEqual(self.suggester.get_suggestion_list(self.user, limit=2), [
            (movie0, factors.FACTOR_IMDB_TOP),
            (movie1, factors.FACTOR_IMDB_TOP),
        ])

        self.user.add_movie(movie0)

        self.assertEqual(self.suggester.get_suggestion_list(self.user, limit=2), [
            (movie1, factors.FACTOR_IMDB_TOP),
            (movie2, factors.FACTOR_IMDB_TOP),
        ])

        self.user.add_movie(movie1)
        self.user.add_movie(movie2)

        self.assertEqual(self.suggester.get_suggestion_list(self.user, limit=2), [
            (movie3, factors.FACTOR_IMDB_TOP),
        ])

        self.user.add_movie(movie3)

        self.assertEqual(self.suggester.get_suggestion_list(self.user, limit=2), [])

    def test_suggestion_list_sames_series_top_priority(self):
        hp = movie_recipes.movie_chain.make(is_direct_series=True)
        hp1 = movie_recipes.movie.make()
        hp2 = movie_recipes.movie.make()
        hp.movies.add(hp1, hp2)

        top_imdb_movie = movie_recipes.movie.make(votes_imdb=1000, rating_imdb=8)

        self.user.add_movie(hp1)

        self.assertEqual(self.suggester.get_suggestion_list(self.user), [
            (hp2, factors.FACTOR_SAME_SERIES),
            (top_imdb_movie, factors.FACTOR_IMDB_TOP),
        ])


