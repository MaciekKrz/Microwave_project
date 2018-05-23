from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# def get_test_with_cache():
#     if 'test' in cache:
#         power = cache.get('test')
#     else:
#         # key = 'test'
#         # with cache.lock(key, expire=60):
#         #     ttl = cache.ttl(key)
#         #     cache.ttl(key, ttl + 10)
#
#         power = 100
#         # recipes = list(Recipe.objects.prefetch_related('ingredient_set__food'))
#         cache.set('test', power, timeout=CACHE_TTL)
#         TTL = cache.ttl('test')
#     return power, TTL