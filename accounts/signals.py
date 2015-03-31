from django import dispatch

user_followed = dispatch.Signal(providing_args=["user", "friend"])
user_unfollowed = dispatch.Signal(providing_args=["user", "friend"])
