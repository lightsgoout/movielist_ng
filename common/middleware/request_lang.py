from django.conf import settings
from django.utils import translation


class RequestLangMiddleware(object):

    def process_request(self, request):
        if 'lang' in request.GET:
            lang = request.GET.get('lang')
            if lang in zip(*settings.LANGUAGES)[0]:
                translation.activate(lang)
