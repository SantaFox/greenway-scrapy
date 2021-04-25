import scrapy


class ItemsSpider(scrapy.Spider):
    name = "new"

    start_urls = [
        'https://rc212.greenwaystart.com/shop/brands/Kits/',
        'https://rc212.greenwaystart.com/shop/brands/Aquamagic/',
        'https://rc212.greenwaystart.com/shop/brands/Aquamatic/',
        'https://rc212.greenwaystart.com/shop/brands/BioTrim/',
        'https://rc212.greenwaystart.com/shop/brands/Sharme-Essential/',
        'https://rc212.greenwaystart.com/shop/brands/TeaVitall/',
        'https://rc212.greenwaystart.com/shop/brands/accessories/',
        'https://rc212.greenwaystart.com/shop/brands/books/',
    ]

    def request(self, url, callback):
        """
         Wrapper for scrapy.request
        """
        request = scrapy.Request(url=url, callback=callback)

        # cyprus_ru = {'CCLLang': 'ru_RU', 'CCLCity': '242683', 'CCLID': 'eu', 'CCLCountry': '44', 'CCLCityName': 'Республика Кипр'}
        # cyprus_en = {'CCLLang': 'en_US', 'CCLCity': '242683', 'CCLID': 'eu', 'CCLCountry': '44', 'CCLCityName': 'Республика Кипр'}
        # russia_ru = {'CCLLang': 'ru_RU', 'CCLCity': '183527', 'CCLID': 'ru', 'CCLCountry': '1', 'CCLCityName': 'Москва'}
        # russia_en = {'CCLLang': 'en_US', 'CCLCity': '183527', 'CCLID': 'ru', 'CCLCountry': '1', 'CCLCityName': 'Moscow'}
        # request.cookies.update(cyprus_ru)

        request.headers['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36')
        return request

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield self.request(url, self.parse_section)

    def parse(self, response):
        items_links = response.css('div.productItem div.productItem__content a.productItem__name::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_section(self, response):
        items_links = response.css('div.productItem div.productItem__content a.productItem__name::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('div.app__container div.row')
        product_details = product_page.css('div.productInfo')
        product_images = product_page.css('div.productInfoImage')
        product_tabs = product_page.css('div.tabs-product')

        name = product_details.css('div.productInfo__title::text').get()
        spec = product_details.css('div.productInfo__small-params::text').get()
        code = product_details.css('div.productInfo__top-code::text').get()

        if name is not None:
            name = name.strip()
        if spec is not None:
            spec = spec.strip()
        if code is not None:
            code = code.strip()

        # pic_fore = product_page.css('div.gallery-slide img::attr(data-zoom-image)').get()
        # if pic_fore is not None:
        #     pic_fore = pic_fore.strip()
        # pics = {response.urljoin(pic_fore)}
        pics = set()
        for pic in product_images.css('a.productInfoImage__preview-image::attr(data-big)').getall():
            pics.add(response.urljoin(pic.strip()))

        # params_raw = product_page.css('div.catalog-item-info p span::text').getall()
        # params = {}
        # for i in range(int(len(params_raw) / 2)):
        #     params[params_raw[i * 2].strip()] = params_raw[i * 2 + 1].strip()
        #
        # price_headers = {'Price', 'Partner price', 'Цена', 'Цена партнёра'}
        # for key in params.keys():
        #     if key in price_headers:
        #         price = params[key].split()[0]

        tab_links = product_tabs.css('div.tabs__header a')
        texts = []
        for tab_info in tab_links:
            tab_id = tab_info.css('a::attr(data-js-tab)').get()
            tab_code = tab_info.css('a::attr(href)').get()
            tab = product_tabs.css('div.tabs__item#'+tab_id.strip()+' div.productDescription')
            tab_nodes = tab.css('div > *').getall()
            tab_text = tab.css('::text').get().strip()
            if tab_text.strip() != '':
                tab_nodes.append(tab_text)
            texts.append({'name': tab_code.strip(), 'text': tab_nodes})

        yield {
            'name': name,
            'spec': spec,
            'code': code,
            # 'price': price,
            'pics': pics,
            # 'params': params,
            'texts': texts,
            'file_urls': pics,
        }
