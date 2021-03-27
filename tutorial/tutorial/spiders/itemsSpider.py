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
        'https://www.mygreenway.eu/products/TeaVitall/',
    ]

    def parse(self, response):
        items_links = response.css('div.catalog-item a.catalog-item-title::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('section.product-page')
        product_details = response.css('section.product-details')

        name = product_page.css('section.page-head h1::text').get().strip()
        spec = product_page.css('div.product-main-info p::text').get().strip()
        code = product_page.css('div.product-main-info h4::text').get().strip()

        params_raw = product_page.css('div.catalog-item-info p span::text').getall()
        params = {}
        for i in range(int(len(params_raw)/2)):
            params[params_raw[i*2]] = params_raw[i*2+1].strip()

        pics = {response.urljoin(product_page.css('div.gallery-slide img::attr(data-zoom-image)').get().strip())}
        for pic in product_page.css('div.gallery-thumb img::attr(data-zoom-image)').getall():
            pics.add(response.urljoin(pic.strip()))

        tabs = product_details.css('ul.nav li a::attr(href)').getall()
        texts = {}
        for tab in tabs:
            texts[tab] = product_details.css('div.tab-content div' + tab + ' > *').getall()

        yield {
            'name': name,
            'spec': spec,
            'code': code,
            'price': params['Price'],
            'pics': pics,
            'params': params,
            'texts': texts,
        }
