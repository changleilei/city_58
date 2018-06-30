# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..utils.parse import parse, \
    xiaoqu_parse,\
    get_ershou_price_list,\
    chuzu_list_get_detail_url,\
    get_chuzu_house_info
from ..items import City58ItemXiaoQu,\
    City58ItemXiaoChuZuQuInfo

from traceback import format_exc
class Spider58CitySpider(scrapy.Spider):
    name = 'spider_58_city'
    allowed_domains = ['58.com']
    host = 'cd.58.com'
    url_format = 'http://{}/xiaoqu/{}/'
    xiaoqu_number = list(range(103, 118))
    xiaoqu_number.append(21611)

    def start_requests(self):
        start_urls = ['http://{}/xiaoqu/{}/'.format(self.host, number)for number in self.xiaoqu_number]
        for url in start_urls:
            yield Request(url)

    def parse(self, response):
        """
        抓取所有小区
        :param response:
        :return:
        """
        url_list = parse(response)#得到小区所有url
        for url in url_list:
            yield Request(url,
                          callback=self.xiaoqu_detail_pag,
                          errback=self.error_back,
                          priority=4)


    def xiaoqu_detail_pag(self, response):
        """
        抓取小区详情页
        :param responce:
        :return:
        """
        _ = self
        data = xiaoqu_parse(response)
        item = City58ItemXiaoQu()
        item.update(data)
        item['id'] = response.url.split('/')[4]

        yield item

        #二手房

        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.ershoufang_list_pag,
                      errback=self.error_back,
                      meta={'id':item['id']},
                      priority=3)

        #出租房
        url_ = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.chuzu_list_pag,
                      errback=self.error_back,
                      meta={'id': item['id']},
                      priority=3)

    def chuzu_list_pag(self,response):
        """
        抓取出租房详情页url
        :param response:
        :return:
        """
        _ = self
        url_list = chuzu_list_get_detail_url(response)

        for url in url_list:
            yield response.request.replace(url,
                                           callback=self.chuzu_detail_pag,
                                           priority = 1)

    def chuzu_detail_pag(self, response):
        """
        出租房详细信息
        :param response:
        :return:
        """
        _ = self
        data = get_chuzu_house_info(response)
        item = City58ItemXiaoChuZuQuInfo()
        item.update(data)
        item['id'] = response.meta['id']
        item['url'] = response.url
        yield item

    def ershoufang_list_pag(self,response):
        """
        二手房详细页面信息
        :param response:
        :return:
        """
        _ = self
        price_list = get_ershou_price_list(response)
        yield {'id':response.meta['id'],'price_list':price_list}
        #可设置翻页



    def error_back(self, e):
        _ = e
        self.logger.error(format_exc())