import scrapy


class ItemsSpider(scrapy.Spider):
    name = "items"

    start_urls = [
        'https://www.mygreenway.eu/products/Aquamagic/',
    ]

    def parse(self, response):
        items_links = response.css('div.catalog-item a.catalog-item-title::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('section.product-page')
        yield {
            'name': product_page.css('section.page-head h1::text').get(),
            'code': product_page.css('div.product-main-info h4::text').get(),
            'pics': product_page.css('div.gallery-thumb img::attr(data-zoom-image)').getall(),
        }