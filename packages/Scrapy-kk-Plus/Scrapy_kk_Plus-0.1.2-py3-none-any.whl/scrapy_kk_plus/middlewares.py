import json

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy_redis import get_redis_from_settings

from .bloomfilter import BloomFilter
from .defaults import BLOOMFILTER_BIT, BLOOMFILTER_HASH_NUMBER


class PermanentFilterMiddleware:
    def __init__(self, settings):
        self.server = get_redis_from_settings(settings)
        bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        key = settings.get("PF_KEY")
        self.bf = BloomFilter(self.server, key, bit, hash_number)


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        settings = crawler.settings
        s = cls(settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        try:
            obj = request.meta['pf_info']
            if obj:
                pf_info = json.loads(obj)
                url = pf_info['url']
                if self.bf.exists(url):
                    raise IgnoreRequest
        except:
            return None

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        # settings = spider.settings
        # server = get_redis_from_settings(settings)
        # bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_BIT)
        # hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', BLOOMFILTER_HASH_NUMBER)
        # key = spider.name + ":pf_bloomfilter"
        # spider.logger.info('Spider item request bloomfilter start...')

        spider.logger.info('Spider opened: %s' % spider.name)
