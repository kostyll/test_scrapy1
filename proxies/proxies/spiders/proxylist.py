# -*- coding: utf-8 -*-
import scrapy
from proxies.items import ProxiesItem
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.selector import HtmlXPathSelector

from lxml import etree


class ProxiesLoader(XPathItemLoader):
    # default_output_processor = TakeFirst()
    pass

class ProxylistSpider(scrapy.Spider):
    name = "proxylist"
    allowed_domains = ["hidemyass.com"]
    start_urls = (
        'http://proxylist.hidemyass.com/',
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        l = ProxiesLoader(ProxiesItem(), hxs)

        items = []

        for tr in hxs.select('//table[@id="listable"]/tbody/tr'):

            print "\n"


            item = ProxiesItem()
            item['port'] = tr.select('./td[3]/text()').extract()[0].strip('\n').strip()
            style = tr.select('./td[2]/span/style/text()')
            styles = { (x.split('{')[0][1:]):('inline' in x) for x in str(style.extract()[0]).split('\n')[1:][:-1]}
            print styles
            ipAddressStr = ""

            mainspan = tr.select('./td[2]/span')
            print "source_tag = %s" % (etree.tostring(mainspan[0].root))
            for i in mainspan[0].root.getchildren():

                print "tag = %s" % i.tag
                print "source = %s" % etree.tostring(i)
                if (
                    (not ("display:none" in i.values())) and
                    (i.tag != "style")
                ):
                    class_ = i.values()
                    print "class_ = %s" % class_
                    if (len(class_) > 0):
                        if styles.get(class_[0], True):
                            text = i.xpath("text()")
                            print "text = %s" % text
                            if (len(text) > 0):
                                ipAddressStr += text[0].strip()

                sibling_text = etree.tostring(i).rpartition(">")[2].strip("\n").strip()
                print "sibling_text = %s" % sibling_text
                ipAddressStr += sibling_text.strip()

                print "->IP = %s " % ipAddressStr

            while (ipAddressStr.find("..")>0):
                ipAddressStr = ipAddressStr.replace("..", ".")
            print "IP = %s " % ipAddressStr

            item['ipAddress'] = ipAddressStr

            items.append(item)

        return items