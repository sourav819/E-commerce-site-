import scrapy
from scrapy import Request

class projIMDB(scrapy.Spider):
    name='boss'
    start_urls=['https://www.hugoboss.com/in/en/home']
    def parse(self,response):
        categoryURl = 'a[href="https://www.hugoboss.com/in/en/men-clothing/"] + div .col-xl-offset-1 a::attr(href)'
        for url in response.css(categoryURl).getall():
            yield Request(url, callback=self.parseProducts)
            break

    def parseProducts(self,response):
        print('--------------------------------')
        productURL= '.product-tile-default__gallery a::attr(href)'
        for produrl in response.css(productURL).getall():
            yield response.follow(produrl, callback=self.parseProduct)
        
        nextPageCSS = '.button--pagingbar.pagingbar__next.font__nav-link::attr(href)'
        nextPageURL = response.css(nextPageCSS).get()
        if nextPageURL:
            yield Request(nextPageURL, callback=self.parseProducts)
        
    def parseProduct(self,response):
        availColour = response.css('.color-selector__text::text').getall()
        productColour = ','.join(availColour)
        productName = response.css('.pdp-stage__header-title::text').get().strip()
        instructions = response.css('div.care-info span::text').getall()
        inst = ','.join(instructions)

        yield {
         'Product Name' : productName,
         'Product Colour' : productColour,
         'Instructions' : inst  
        }
