from django import dispatch

achievement_unlocked = dispatch.Signal(providing_args=["user", "achievement"])
achievement_locked = dispatch.Signal(providing_args=["user", "achievement"])
