import scrapy


class GreekSpider(scrapy.Spider):
    name = "greek"

    start_urls = [
        'https://mygreenway.gr/aquamagic-category/',
        'https://mygreenway.gr/aquamatic/',
        'https://mygreenway.gr/biotrim/',
        'https://mygreenway.gr/aquamagic-plush/',
        'https://mygreenway.gr/essential-sharme/',
        'https://mygreenway.gr/tea-vitall/',
    ]

    def parse(self, response):
        items_links = response.css('div.col-md-4 > a.link::attr(href), div.col-md-3 > a.link::attr(href)')
        yield from response.follow_all(items_links, self.parse_item)

    def parse_item(self, response):
        product_page = response.css('div.content#content div.wpb_row:nth-child(2)')
        left = product_page.css('div.wpb_column.vc_column_container.vc_col-sm-6:first-child')
        right = product_page.css('div.wpb_column.vc_column_container.vc_col-sm-6:nth-child(2)')

        name = right.css('h2.vc_custom_heading::text, h3.vc_custom_heading::text, h4.vc_custom_heading::text').get()
        # spec = product_page.css('div.product-main-info p::text').get()
        code = right.css('div.vc_custom_heading::text').get()
        desc = right.css('div.wpb_content_element div.wpb_wrapper:first-child > *').getall()
        price = right.css('div.wpb_content_element div.wpb_wrapper:nth-child(2)::text').get()

        blocks = right.css('div.wpb_text_column.wpb_content_element div.wpb_wrapper')
        desc = blocks.css('div.wpb_wrapper > *').getall()
        price = ''.join(blocks.css('div.wpb_wrapper::text').getall()).strip()

        #params_raw = product_page.css('div.catalog-item-info p span::text').getall()
        #params = {}
        #for i in range(int(len(params_raw)/2)):
        #    params[params_raw[i*2]] = params_raw[i*2+1]

        #pics = {response.urljoin(product_page.css('div.gallery-slide img::attr(data-zoom-image)').get())}
        #for pic in product_page.css('div.gallery-thumb img::attr(data-zoom-image)').getall():
        #    pics.add(response.urljoin(pic))

        #tabs = product_details.css('ul.nav li a::attr(href)').getall()
        #texts = {}
        #for tab in tabs:
        #    texts[tab] = product_details.css('div.tab-content div' + tab + ' > *').getall()

        yield {
            'name': name,
        #    'spec': spec,
            'code': code,
            'desc': desc,
            'price': price,
        #    'price': params['Price'],
        #    'pics': pics,
        #    'params': params,
        #    'texts': texts,
        }
