# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymysql
import pandas as pd
import urllib.parse
from ..items import PageItem
import requests
import re
from lxml import etree
import datetime
import random
from ..settings import USER_AGENTS



def get_search_content():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='test', passwd='styd', db='reptile', charset='utf8')
        search_content_sql = "select distinct source_id,content  from search_content where source_id=1 and status=1;"
        city_sql = "select source_id,city_num  from city where source_id=1 and status=1 and city_num <500  and city_num>=100;"
        # city_sql = "select source_id,city_num  from city where source_id=1 and status=1 and city_num=2;"
        search_content = pd.read_sql_query(search_content_sql, conn)
        citys = pd.read_sql_query(city_sql, conn)
        content = citys.merge(search_content,how='left',on='source_id').loc[:,['city_num','content']]
        conn.close()
        start_urls = ['http://www.dianping.com/search/keyword/%s/0_%s' % (num, urllib.parse.quote(key)) for num, key
                  in content.get_values()]
        return start_urls
    except Exception as e:
        print(e)
        return []


def get_ip_df():
    from get_ip_from_network import Poor_Ip
    ip_poor = Poor_Ip()
    ip_df = ip_poor.get_poor()

    ip_df['proxy'] = ip_df.apply(lambda x: 'http://' + str(x['ip']) + ':' + str(x['port']),axis=1)




class SearchPageSpider(CrawlSpider):
    name = 'dianping_search_page'
    allowed_domains = ['www.dianping.com']
    now = str(datetime.datetime.now())[:19]
    HEADERS = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Keep-Alive': 'timeout=5',
        'Host': 'www.dianping.com',
        'Referer': 'https://www.dianping.com/',
        'Cache-Control': 'no-cache',
        'unionid': '16b266666e0c8-06af461b9ac245-50432518-144000-16b266666e1c8',
        'Cookies': 'cye=shanghai; Domain=.dianping.com; Expires=Sun, 14-Jul-2019 08:58:54 GMT; Path=/',
    }
    # start_urls = ['https://www.dianping.com/search/keyword/1735/0_%E5%81%A5%E8%BA%AB']
    page_link = LinkExtractor(
        restrict_xpaths=(r'//div[@class="content-wrap"]/div[@class="shop-wrap"]/div[@class="page"]/a'))
        # restrict_xpaths=(r'/html/body/div[2]/div[3]/div[1]/div[2]/a[11]'))
    rules = (
        Rule(page_link,
             callback='parse_item', follow=True),
    )

    def start_requests(self):
        start_urls = get_search_content()
        for url in start_urls:
            HEADERS = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'www.dianping.com',
                'unionid': '16b266666e0c8-06af461b9ac245-50432518-144000-16b266666e1c8',
            }
            proxy = random.choice(list(pd.read_excel('ip_address.xlsx').ip_address))
            # proxy = random.choice(list(ip_df.proxy))
            print(proxy)
            print(url)
            yield scrapy.Request(url, callback=self.parse,headers=HEADERS, dont_filter=False,meta={'proxy': proxy})
            # yield scrapy.Request(url, callback=self.parse, headers=HEADERS, dont_filter=False)

    def parse_item(self, response):
        shop_list_url = response.url
        print("--------------------------------------------------------------------")
        print(shop_list_url)
        # 判断该页面是否被爬取过
        url_is_get = self.get_page_status(response.url)
        if url_is_get:
            try:
                link_list = response.xpath('//div[@id="shop-all-list"]/ul/li/div[@class="txt"]//a[@data-hippo-type="shop"]')
                if len(link_list) == 0:
                    yield scrapy.Request(url=shop_list_url, callback=self.parse_item_callback,headers=self.HEADERS)
                else:
                    is_search = response.xpath('//div[@class="not-found"]//div[@class="not-found-words"]')
                    # 用于判断爬取页面是否有内容
                    if len(is_search) != 0:
                        pass
                    else:
                        # 更新page的状态
                        self.update_page_status(shop_list_url)
                        for i in range(len(link_list)):
                            item = PageItem()
                            link = etree.HTML(link_list[i].extract())
                            shop = link.xpath('//a/@href')[0]
                            shop_id = shop.split('/')[-1]
                            item['shop_id'] =shop_id
                            item['shop_url'] =shop
                            item['city_id'] = shop_list_url.split('keyword/')[1].split('/')[0]
                            if self.get_shop_status(shop_id, shop):
                                yield item
                                pass
                            else:
                                print("该门店基础信息已经爬取过了！")
                                pass
            except Exception as e:
                print(e)
                pass
        else:
            print("该页面已经爬取过！")
            pass

    def parse_item_callback(self, response):
        shop_list_url = response.url
        # 判断该页面是否被爬取过
        url_is_get = self.get_page_status(response.url)
        if url_is_get:
            try:
                link_list = response.xpath(
                    '//div[@id="shop-all-list"]/ul/li/div[@class="txt"]//a[@data-hippo-type="shop"]')
                if len(link_list) == 0:
                    yield scrapy.Request(url=shop_list_url, callback=self.parse_item_callback,headers=self.HEADERS)
                else:
                    is_search = response.xpath('//div[@class="not-found"]//div[@class="not-found-words"]')
                    # 用于判断爬取页面是否有内容
                    if len(is_search) != 0:
                        pass
                    else:
                        # 更新page的状态
                        self.update_page_status(shop_list_url)
                        for i in range(len(link_list)):
                            item = PageItem()
                            link = etree.HTML(link_list[i].extract())
                            shop = link.xpath('//a/@href')[0]
                            shop_id = shop.split('/')[-1]
                            item['shop_id'] = shop_id
                            item['shop_url'] = shop
                            if self.get_shop_status(shop_id, shop):
                                yield item
                            else:
                                print("该门店基础信息已经爬取过了！2")
                                pass

            except Exception as e:
                print(e)
                pass
        else:
            print("该页面已经爬取过！")
            pass

    # 用于判断该页面是否被爬取过;没爬过True；爬过False
    def get_page_status(self, search_page_url):
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='test', passwd='styd', db='reptile',
                                   charset='utf8')
            search_sql = "select distinct is_get  from  search_page_url where source_id=1 and  search_page_url ='%s' ;" % (
            search_page_url)
            city_id = search_page_url.split('keyword/')[1].split('/')[0]
            search_content = pd.read_sql_query(search_sql, conn)
            if len(search_content) == 0:
                sql = "insert into search_page_url (source_id,search_page_url,city_id,is_get,created_time,updated_time) values(1,'%s',%s,0,'%s','%s');" % (
                search_page_url,city_id,self.now, self.now)
                print(sql)
                conn.query(sql=sql)
                conn.commit()
                conn.close()
                return True
            else:
                if search_content.is_get[0] == 1:
                    conn.close()
                    return False
                else:
                    conn.close()
                    return True
        except Exception as e:
            print(e)
            return False

    # 用于判断该页面是否被爬取
    def update_page_status(self, search_page_url):
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='test', passwd='styd', db='reptile',
                                   charset='utf8')
            search_sql = "update search_page_url set is_get=1 where source_id=1 and search_page_url='%s';" % (
            search_page_url)
            conn.query(search_sql)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

    # 用于判断该门店是否被爬取
    def get_shop_status(self, shop_id, shop_url):
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='test', passwd='styd', db='reptile',
                                   charset='utf8')
            search_sql = "select distinct is_get  from  data_shop where  source_id=1 and  shop_id ='%s' ;" % (
            shop_id)
            search_content = pd.read_sql_query(search_sql, conn)
            conn.close()
            if len(search_content) == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


