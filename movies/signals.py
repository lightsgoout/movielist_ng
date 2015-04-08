from django import dispatch

user_added_movie = dispatch.Signal(providing_args=["user", "movie", "status", "score"])
user_removed_movie = dispatch.Signal(providing_args=["user", "movie", "status", "score"])
user_scored_movie = dispatch.Signal(providing_args=["user", "movie", "score"])
user_changed_score = dispatch.Signal(providing_args=["user", "movie", "new_score", "old_score"])
