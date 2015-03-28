WATCHED = 'W'
PLAN_TO_WATCH = 'P'
IGNORED = 'I'

STATUS_CHOICES = (
    (WATCHED, 'Watched'),
    (PLAN_TO_WATCH, 'Plan to watch'),
    (IGNORED, 'Ignored'),
)

# Movie with this score or higher considered "approved" when making comparisons
COMPATIBILITY_MOVIE_APPROVED_SCORE = 7
# Compatibility can be calculated when both users has this minimum movies:
COMPATIBILITY_MINIMUM_MOVIES_REQUIRED = 10
