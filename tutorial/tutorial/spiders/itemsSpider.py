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
        # 'https://www.mygreenway.eu/products/Gift-sets/',          почему-то пропала в марте 2021
        'https://www.mygreenway.eu/products/TeaVitall/',
    ]

    def request(self, url, callback):
        """
         Wrapper for scrapy.request
        """
        request = scrapy.Request(url=url, callback=callback)

        cyprus_ru = {'CCLLang': 'ru_RU', 'CCLCity': '242683', 'CCLID': 'eu', 'CCLCountry': '44', 'CCLCityName': 'Республика Кипр'}
        cyprus_en = {'CCLLang': 'en_US', 'CCLCity': '242683', 'CCLID': 'eu', 'CCLCountry': '44', 'CCLCityName': 'Республика Кипр'}
        russia_ru = {'CCLLang': 'ru_RU', 'CCLCity': '183527', 'CCLID': 'ru', 'CCLCountry': '1', 'CCLCityName': 'Москва'}
        russia_en = {'CCLLang': 'en_US', 'CCLCity': '183527', 'CCLID': 'ru', 'CCLCountry': '1', 'CCLCityName': 'Moscow'}
        request.cookies.update(cyprus_en)

        request.headers['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36')
        return request

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield self.request(url, self.parse_section)

    def parse(self, response):
        items_links = response.css('div.catalog-item a.catalog-item-title::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_section(self, response):
        items_links = response.css('div.catalog-item a.catalog-item-title::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('section.product-page')
        product_details = response.css('section.product-details')

        name = product_page.css('section.page-head h1::text').get()
        spec = product_page.css('div.product-main-info p::text').get()
        code = product_page.css('div.product-main-info h4::text').get()

        if name is not None:
            name = name.strip()
        if spec is not None:
            spec = spec.strip()
        if code is not None:
            code = code.strip()

        pic_fore = product_page.css('div.gallery-slide img::attr(data-zoom-image)').get()
        if pic_fore is not None:
            pic_fore = pic_fore.strip()
        pics = {response.urljoin(pic_fore)}
        for pic in product_page.css('div.gallery-thumb img::attr(data-zoom-image)').getall():
            pics.add(response.urljoin(pic.strip()))

        params_raw = product_page.css('div.catalog-item-info p span::text').getall()
        params = {}
        for i in range(int(len(params_raw) / 2)):
            params[params_raw[i * 2].strip()] = params_raw[i * 2 + 1].strip()

        price_headers = {'Price', 'Partner price', 'Цена', 'Цена партнёра'}
        for key in params.keys():
            if key in price_headers:
                price = params[key].split()[0]

        tabs = product_details.css('ul.nav li a::attr(href)').getall()
        texts = {}
        for tab in tabs:
            texts[tab.strip()] = product_details.css('div.tab-content div' + tab.strip() + ' > *').getall()

        yield {
            'name': name,
            'spec': spec,
            'code': code,
            'price': price,
            'pics': pics,
            'params': params,
            'texts': texts,
            'image_urls': pics,
        }
