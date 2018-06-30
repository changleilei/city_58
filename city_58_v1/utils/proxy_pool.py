from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import requests
def get_ip_list():
    url = 'http://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')
    ip_text = bsObj.findAll('tr', {'class': 'odd'})   # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
        ip_list.append(ip_port)
    test_url = 'http://cd.58.com/zufang/'  # 这只是一个用来测试的网址，可以修改为目标网站

    proxies_pool = []  # 初始化一个代理池列表

    for ip_test in ip_list:  # 遍历一下爬取下来的IP列表 # 取出跟IP相对应的端口

        proxies = {
            'http': 'http://{}'.format(ip_test),
            'https': 'http://{}'.format(ip_test),
        }
        try:  # 异常处理
            response1 = requests.get(test_url, proxies=proxies, timeout=3)
            if response1.status_code == 200:
                proxies_pool.append({ip_test})
                print('代理IP{}已保存！'.format(ip_test))
            else:
                print('代理IP请求不成功！')
        except:
                print('代理IP无效！')

    print("共收集到了{}个代理IP".format(len(proxies_pool)))
    return proxies_pool


if __name__ == '__main__':
    get_ip_list()