import redis
from django.utils import timezone

REDIS_CACHE = redis.Redis()


def set_last_login(user_id):
    user_last_active_time = f"user:{user_id}:last_login"
    last_update_time = timezone.now().isoformat().encode("utf-8")
    REDIS_CACHE.set(user_last_active_time, last_update_time)
