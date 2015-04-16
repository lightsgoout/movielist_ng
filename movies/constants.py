WATCHED = 'W'
PLAN_TO_WATCH = 'P'
IGNORED = 'I'

STATUS_CHOICES = (
    (WATCHED, 'Watched'),
    (PLAN_TO_WATCH, 'Plan to watch'),
    (IGNORED, 'Ignored'),
)

# Movie with this score or higher considered "approved" when making comparisons
COMPATIBILITY_MOVIE_APPROVED_SCORE = 8
# Compatibility can be calculated when both users has this minimum movies:
COMPATIBILITY_MINIMUM_MOVIES_REQUIRED = 10
# How many shared movies show below compatibility-meter.
COMPATIBILITY_SHARED_MOVIES_COUNT = 5


COMPARE_MODE_SHARED = 'S'
COMPARE_MODE_UNIQUE_LEFT = 'L'
COMPARE_MODE_UNIQUE_RIGHT = 'R'
COMPARE_MODE_SCORE_DISTRIBUTION = 'SCORE_DISTR'
