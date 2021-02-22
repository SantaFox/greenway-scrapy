import scrapy


class ItemsSpider(scrapy.Spider):
    name = "items"

    start_urls = [
        'https://www.mygreenway.eu/products/Aquamagic/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes={page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

'''item = response.css('div.catalog-item')[0]
item.css('div.catalog-item-code::text').get()
item.css('a.catalog-item-title::attr(href)').get()
'''