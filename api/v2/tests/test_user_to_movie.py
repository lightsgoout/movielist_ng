from django.core.urlresolvers import reverse
import mock
from tastypie.test import ResourceTestCase
from accounts import mommy_recipes as accounts_recipes
from movies import mommy_recipes as movie_recipes, constants


class TestUserToMovieResource(ResourceTestCase):

    def setUp(self):
        super(TestUserToMovieResource, self).setUp()
        self.user = accounts_recipes.user.make()
        self.user.set_password('123')
        self.user.save()

        self.assertTrue(
            self.api_client.client.login(
                username=self.user.username,
                password='123'
            )
        )

    # def test_put_movie_readonly(self):
    #     movie = movie_recipes.movie.make(year=2005)
    #     user_to_movie = self.user.add_movie(movie)
    #
    #     detail_url = reverse(
    #         'api_dispatch_detail',
    #         kwargs={'resource_name': 'user_to_movie', 'pk': user_to_movie.pk}
    #     )
    #
    #     resp = self.api_client.get(detail_url)
    #     self.assertValidJSONResponse(resp)
    #     data = self.deserialize(resp)
    #
    #     data['movie']['year'] = 2003
    #     resp = self.api_client.put(detail_url, data=data)
    #     self.assertHttpUnauthorized(resp)

    # def test_authorization(self):
    #     """
    #     User can only update his own records
    #     """
    #     another_user = accounts_recipes.user.make()
    #     movie = movie_recipes.movie.make()
    #     user_to_movie = another_user.add_movie(movie)
    #
    #     detail_url = reverse(
    #         'api_dispatch_detail',
    #         kwargs={'resource_name': 'user_to_movie', 'pk': user_to_movie.pk}
    #     )
    #
    #     resp = self.api_client.get(detail_url)
    #     self.assertValidJSONResponse(resp)
    #     data = self.deserialize(resp)
    #
    #     data['score'] = 3
    #     resp = self.api_client.put(detail_url, data=data)
    #     self.assertHttpUnauthorized(resp)

    def test_add_movie(self):
        movie = movie_recipes.movie.make()
        user_to_movie = movie_recipes.user_to_movie.make()
        url = reverse('api_add_movie', kwargs={'resource_name': 'movie_actions'})

        with mock.patch('accounts.models.MovielistUser.add_movie') as m_add_movie:
            m_add_movie.return_value = user_to_movie
            resp = self.api_client.post(url, data={
                'movie_id': movie.id,
                'status': constants.WATCHED,
            })

            m_add_movie.assert_called_once_with(
                movie,
                constants.WATCHED
            )

            self.assertHttpOK(resp)
            pass
