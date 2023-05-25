import redis
from django.utils import timezone

REDIS_CACHE = redis.Redis()


def check_last_login(user_id):
    r = redis.Redis()
    user_last_active_time_key_identifier = f"user:{user_id}:last_login"
    last_update_time = timezone.now().isoformat()
    r.set(user_last_active_time_key_identifier, last_update_time)
