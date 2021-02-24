import scrapy


class ItemsSpider(scrapy.Spider):
    name = "items"

    start_urls = [
        'https://www.mygreenway.eu/products/Kits/',
        'https://www.mygreenway.eu/products/Aquamagic/',
        'https://www.mygreenway.eu/products/Aquamatic/',
        'https://www.mygreenway.eu/products/BioTrim/',
        'https://www.mygreenway.eu/products/Plush/',
        'https://www.mygreenway.eu/products/accessories/',
        'https://www.mygreenway.eu/products/books/',
        'https://www.mygreenway.eu/products/Sharme-Essential/',
        'https://www.mygreenway.eu/products/Gift-sets/',

    ]

    def parse(self, response):
        items_links = response.css('div.catalog-item a.catalog-item-title::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('section.product-page')
        yield {
            'name': product_page.css('section.page-head h1::text').get(),
            'size': product_page.css('div.product-main-info p::text').get(),
            'code': product_page.css('div.product-main-info h4::text').get(),
            'pics': product_page.css('div.gallery-thumb img::attr(data-zoom-image)').getall(),
            'params': product_page.css('div.catalog-item-info p span::text').getall()
        }

        product_details = response.css('section.product-details')
        yield {
            'tabs': product_details.css('ul.nav li a::attr(href)').get(),
            'text': product_details.css('div.tab-content div#description').get(),
        }