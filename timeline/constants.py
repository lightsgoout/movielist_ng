USER_WATCHED_MOVIE = 0
USER_PLAN_TO_WATCH_MOVIE = 1
USER_FOLLOWED = 2
ACHIEVEMENT_UNLOCKED = 3
ACHIEVEMENT_LOCKED = 4
USER_SCORED_MOVIE = 5
USER_FOLLOWING = 6

EVENT_TYPE_CHOICES = (
    (USER_WATCHED_MOVIE, 'User watched movie'),
    (USER_PLAN_TO_WATCH_MOVIE, 'User planned to watch movie'),
    (USER_FOLLOWED, 'User followed another user'),
    (ACHIEVEMENT_UNLOCKED, 'Achievement unlocked'),
    (ACHIEVEMENT_LOCKED, 'Achievement locked'),
    (USER_SCORED_MOVIE, 'User scored movie'),
    (USER_FOLLOWING, 'User following'),
)

