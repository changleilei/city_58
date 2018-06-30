# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .utils.proxy_pool import get_ip_list

proxy_pool = get_ip_list()
class ProxyMiddleware(object):

    def process_request(self, request, spider):
        #传入代理服务器，下面语句需要替换为自己的代理方式
        request.meta['proxy'] = 'http://{}'.format((proxy_pool.pop()))
        print()



