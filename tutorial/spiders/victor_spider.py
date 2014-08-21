#from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy
from tutorial.items import ProductItem
from scrapy.selector import HtmlXPathSelector
import re

class VicSpider(scrapy.Spider):
    name = "Victoria"
    allowed_domains = ["victoriassecret.com"]
    start_urls = [
        "https://www.victoriassecret.com/sleepwear/lingerie/lace-bustle-back-slip-sexy-little-things?ProductID=175749&CatalogueType=OLS",
        "https://www.victoriassecret.com/bras/new-simple-sexy-a/perfect-shape-bra-the-t-shirt?ProductID=202104&CatalogueType=OLS"
        #"https://www.victoriassecret.com"
    ]
 #   rules = [
        #Rule(SgmlLinkExtractor(allow=('\?ProductID[\S]+', )), follow=True)
    #]

    def parse(self,response):
        sel = HtmlXPathSelector(response)
        item = ProductItem()
        #str = sel.xpath("//div[@class='name']/hgroup/h1/text()").extract()

        item['title'] = sel.xpath("//div[@class='name']/hgroup/h1/text()").extract()
        item['description'] = sel.xpath("//div[@class='full']//text()").extract()[0]
        item['details'] = sel.xpath("//div[@id='description']//ul/li//text()").extract()

        item['images'] = sel.xpath("//img[@id='vsImage']/@src").extract()
        item['imagesdata'] = sel.xpath("//ul[@class='pdp-info box split primary']//section[@class='swatches module']/div[@class='swap']//span[@data-alt-image]/@data-alt-image").extract()

        item['prices'] = map(unicode.strip,sel.xpath("//ul[@class='pdp-info box split primary']/li//div[@class='price']/p/text()").extract())[0]
        item['colors'] = sel.xpath("//ul[@class='pdp-info box split primary']//section[@class='swatches module']/div[@class='swap']//h4/text()").extract()
        item['sizes'] = sel.xpath("//ul[@class='pdp-info box split primary']//div[@class=' scroll']//a//span/text()").extract()[1:]


        item['id'] = sel.xpath("//section[@class='product']/@data-id").extract()[0]

        str = sel.xpath("//script//text()").extract()
        for i in str:
            res = re.findall('\{\"assetId\".*?\"R\"\}',i)
            if res != []:
                item['data'] = res

        yield item



