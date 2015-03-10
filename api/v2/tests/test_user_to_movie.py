from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCase
from accounts import mommy_recipes as accounts_recipes
from movies import mommy_recipes as movie_recipes


class TestUserToMovieResource(ResourceTestCase):

    def setUp(self):
        super(TestUserToMovieResource, self).setUp()
        self.user = accounts_recipes.user.make()

    def test_put_movie_readonly(self):
        movie = movie_recipes.movie.make(year=2005)
        user_to_movie = self.user.add_movie(movie)

        detail_url = reverse(
            'api_dispatch_detail',
            kwargs={'resource_name': 'user_to_movie', 'pk': user_to_movie.pk}
        )

        resp = self.api_client.get(detail_url)
        self.assertValidJSONResponse(resp)
        data = self.deserialize(resp)

        data['movie']['year'] = 2003
        resp = self.api_client.put(detail_url, data=data)
        self.assertHttpAccepted(resp)

        resp = self.api_client.get(detail_url)
        self.assertValidJSONResponse(resp)
        self.assertDictContainsSubset({
            'year': 2005,
        }, self.deserialize(resp)['movie'])