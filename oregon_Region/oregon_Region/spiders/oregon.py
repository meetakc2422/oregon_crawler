import scrapy
from scrapy.http import Request

class Oregon(scrapy.Spider):
    name = 'or'
    # allowed_domains = ['gov.oregonlive.com/bill/']
    start_urls = ['https://gov.oregonlive.com/bill/intro/2021/page-1/']
    def parse(self, response):
        try:
            bills = response.xpath('//div[@class="indvote"]/a/text()').extract()
            billsUrl = response.xpath('//div[@class="indvote"]/a/@href').extract()
            for i,j in zip(billsUrl,range(len(bills))):
                abs_url = "https://gov.oregonlive.com" + i
                yield Request(url=abs_url,callback=self.parse_more,meta={
                    'Bills':bills[j]
                    })
        except Exception as e:
            return e
        ## next page
        try:
            next_page = response.xpath('//div[@id="nextpage"]/a[last()]/@href').extract_first()
            abs_next_page = "https://gov.oregonlive.com" + next_page
            yield Request(url=abs_next_page)
        except Exception as e:
            return e

    def parse_more(self,response):
        doc_url = response.xpath('//div[@class="billtext"]/ul/li[2]/a/@href').extract_first()
        if 'Doc_Url' not in response.meta:
            response.meta['Doc_Url'] =doc_url
        else:
            response.meta['Doc_Url'].append(doc_url)
        yield response.meta