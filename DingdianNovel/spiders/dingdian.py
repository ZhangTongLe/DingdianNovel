import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request #一个单独的request模块，需要跟进的url的时候，能够用到它
from DingdianNovel.items import DingdiannovelItem

class Dingdianspider(scrapy.Spider):

    name = 'dingdiannovel'
    allowed_domains = ['23us.com'] #用到完全地址会怎样？？
    bash_url = 'http://www.23us.com/class/'
    bashurl = '.html'
    '''
    #这个函数是自带的函数，具体的作用是什么？？
    def start_requests(self):

        #for i in range(1,11):
        for i in range(9,10):
            #这里的self指的是类的实例
            url = self.bash_url + str(i) + '_1' + self.bashurl
            #使用了导入的Request包，来跟进我们的URL
            # （并将返回的response作为参数传递给self.parse, 嗯！这个叫回调函数
            yield Request(url, self.parse)
        #专门用于爬取全本这个类别。但是原本的程序有问题。全本类别网址特殊
        #yield Request('http://www.23us.com/quanben/1', self.parse)

    #接受从start_requests传过来的response，并且处理
    #得到了某个类别小说的全部网站
    def parse(self, response):

        #通过response.xpath获得一个list
        max_num = response.xpath('//div[@class = "pagelink"]/a[@class = "last"]/text()').extract()
        bashurl = str(response.url)[:-7]
        #for num in range(1, int(max_num[0]) + 1):
        for num in range(1, int(max_num[0])):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url, callback=self.get_name)

    #获取到书名以及链接
    def get_name(self, response):

        tds = response.xpath('//tr[@bgcolor = "#ffffff"]').extract()
        for td in tds:
            novelname = td.xpath('td[1]/a/text()').extract()
            novelurl = td.xpath('td[1]/a/@href').extract()
            novelid = novelurl[25:]
            print(novelurl)
            print(novelname)
            yield Request(novelurl, callback=self.get_chapterurl,
                          meta={'name': novelname, 'url': novelurl, 'id': novelid})

    #获取电子书其余的属性信息
    def get_chapterurl(self, response):

        item = DingdiannovelItem()
        #收集从上一个界面传过来的name以及novelurl信息
        item['name'] = str(response.meta['name'])
        item['novelurl'] = response.meta['url']
        item['name_id'] = response.meta['id']
        #收集新的界面上的作者，连载状态，连载字数，类别,id
        author = response.xpath('//table[@id = "at"]/tbody/tr[1]/td[2]')
        serialstatus = response.xpath('//table[@id = "at"]/tbody/tr[1]/td[3]')
        serialnumber = response.xpath('//table[@id = "at"]/tbody/tr[2]/td[2]')
        category = response.xpath('//table[@id = "at"]/tbody/tr[1]/td[1]/a/text()')
        item['anthor'] = author[0]
        item['sertalstatus'] = serialstatus[0]
        item['serialnumber'] = serialnumber[0]
        item['category'] = category[0]
        print("总得输出点什么")
        print(item['name'])
        return item

#robot协议已经改成false
#最后一个界面有的类别爬去不到，先改一改
'''
    def start_requests(self):
        for i in range(9,10):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_ = 'pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1, int(max_num)):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url, callback=self.get_name)
            
    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl, callback=self.get_chapterurl,
                          meta={'name': novelname, 'url': novelurl})

    def get_chapterurl(self, response):
        item = DingdiannovelItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        category = BeautifulSoup(response.text, 'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[1].get_text()
        bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').find('a', class_='read')['href']
        name_id = str(bash_url)[-6:-1].replace('/', '')
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('\xa0', '')
        item['name_id'] = name_id
        return item

