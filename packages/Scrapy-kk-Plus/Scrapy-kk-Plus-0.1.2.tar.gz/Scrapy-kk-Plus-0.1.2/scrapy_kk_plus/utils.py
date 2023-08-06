import redis

from .bloomfilter import BloomFilter


class PermanentFilterManager:
    def __init__(self, redis_host, redis_port, redis_password, pf_key, bit, hash_number):
        _pool = redis.ConnectionPool(host=redis_host, port=int(redis_port),
                                     password=redis_password,
                                     decode_responses=True)
        self._r = redis.Redis(connection_pool=_pool)
        self.bf = BloomFilter(self._r, pf_key, bit, hash_number)

    def add(self, url):
        self.bf.insert(url)
