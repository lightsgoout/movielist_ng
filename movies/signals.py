from django import dispatch

user_watched_movie = dispatch.Signal(providing_args=["user", "movie", "score"])
user_removed_movie = dispatch.Signal(providing_args=["user", "movie", "score"])
