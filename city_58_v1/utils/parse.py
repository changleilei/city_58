# coding UTF-8
from pyquery import PyQuery

def parse(response):
    """
    抓取小区列表页面：
    :param response:
    :return:所有小区URL
    """
    jpy = PyQuery(response.text)

    tr_list = jpy('#infolist > div.listwrap > table > tbody > tr').items()
    result = set()
    for tr in tr_list:
        url = tr('td.info > ul > li.tli1 > a').attr('href')
        result.add(url)
    return result

def xiaoqu_parse(response):
    """
    返回这个小区详细的dict字典，主要包括小区名称，参考房价，小区地址，建筑年代
    :param response:
    :return:
    """
    result = dict()
    jpy = PyQuery(response.text)
    result['name'] = jpy('body > div.body-wrapper > div.title-bar > span.title').text()
    result['reference_pice'] = jpy('body > div.body-wrapper > div.basic-container > '
                                'div.info-container > div.price-container > span.price').text()
    result['address'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container >'
                            ' div.info-tb-container > table > tr:nth-child(1) > td:nth-child(4)').text()
    result['time'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container >'
                         ' div.info-tb-container > table > tr:nth-child(5) > td:nth-child(2)').text()

    return result

def get_ershou_price_list(response):
    """
    匹配房价信息，返回一个list
    :param response:
    :return:
    """
    jpy = PyQuery(response.text)
    price_tag = jpy('td.tc > span:nth-child(3)').text().split()
    price_tag=[i[:-3] for i in price_tag]
    return price_tag

def chuzu_list_get_detail_url(response):
    """
    出租列表页面详情页url
    :param response:
    :return:
    """
    jpy = PyQuery(response.text)
    a_list = jpy('tr> td.t > a.t').items()
    url_list = [a.att('href') for a in  a_list]
    return url_list

def get_chuzu_house_info(response):
    """
    获取出租详情页的相关信息
    返回一个dict包含：出租页标题，出租价格，房屋面积，房屋类型（几室几厅）
    :param:response
    :return:
    """
    jpy = PyQuery(response.text)
    result = dict()
    result['name'] = jpy('body > div.main-wrap > div.house-title > h1').text()
    result['zu_price'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > '
                          'div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b').text()

    result['type'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc'
                         ' > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span:nth-child(2)').text()

    result['type'], result['mianji'], *_ = result['type'].split()
    return result


if __name__ == '__main__':
    import requests
    r = requests.get('http://cd.58.com/zufang/34559406386484x.shtml')
    get_chuzu_house_info(r)
