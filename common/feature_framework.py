import contextlib
import functools


@contextlib.contextmanager
def enabled(feature):
    from django.conf import settings
    try:
        if feature in settings.ENABLED_FEATURES:
            yield True
        else:
            yield False
    except:
        raise


def is_enabled(feature):
    def decorator(func):
        functools.wraps(func)

        def wrapper(*args, **kwargs):
            from django.conf import settings
            if feature in settings.ENABLED_FEATURES:
                return func(*args, **kwargs)
            return None

        return wrapper

    return decorator


def feature_enabled(feature):
    from django.conf import settings
    return feature in settings.ENABLED_FEATURES
