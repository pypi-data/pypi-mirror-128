from scrapy_redis import get_redis_from_settings

from .bloomfilter import BloomFilter
from .defaults import BLOOMFILTER_BIT, BLOOMFILTER_HASH_NUMBER


class PermanentFilterPipeline:
    def __init__(self, bf):
        self.bf = bf

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        server = get_redis_from_settings(settings)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        key = settings.get("PF_KEY") + ":pf_bloomfilter"
        bf = BloomFilter(server, key, bit, hash_number)

        return cls(bf)

    def process_item(self, item, spider):
        try:
            if item['pf_info']:
                self.bf.insert(item['pf_info']['url'])
        except:
            pass
