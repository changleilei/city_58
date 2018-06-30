from pyquery import PyQuery as pq

if __name__=='__main__':
    doc = pq(url="http://cd.58.com/xiaoqu/shenxianshudayuan/")
    print(doc('body > div.body-wrapper > div.basic-container > div.info-container >'
                         ' div.info-tb-container > table > tr:nth-child(5)').text().split())

