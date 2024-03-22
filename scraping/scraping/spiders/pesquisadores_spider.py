import scrapy

from scraping.items import PesquisadoresItem


class PesquisadoresSpider(scrapy.Spider):
    name = 'pesquisadores'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'FEEDS': {
            'data/pesquisadores.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'fields': ['slug', 'nome', 'ano', 'areas', 'projetos', 'url_perfil'],
                'overwrite': True
            }
        },
        'ITEM_PIPELINES': {
            'scraping.pipelines.CustomImagesPipeline': 1
        },
        'IMAGES_STORE': 'data/images'
    }

    def start_requests(self):
        urls = [f'https://serrapilheira.org/pesquisadores/?sf_paged={i}' for i in range(1, 15)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pesquisadores = response.xpath('//li[contains(@class, "pesquisador")]')

        if not pesquisadores:
            return

        for pesquisador in pesquisadores:
            projetos = list()

            for projeto in pesquisador.xpath('.//*[@class="projeto-pesquisador"]/text()').getall():
                projetos.append({
                    'titulo': projeto[0:projeto.rindex('(') - 1],
                    'anos': list(map(int, projeto[projeto.rindex('(') + 1:projeto.rindex(')')].split('/')))
                })

            yield PesquisadoresItem(
                slug=pesquisador.xpath('a/@href').get().strip('/').split('/')[-1],
                nome=pesquisador.xpath('.//h3/text()').get().strip(),
                ano=int(pesquisador.xpath('@data-item-year').get()),
                areas=[area.strip() for area in pesquisador.xpath('.//*[@class="areas-pesquisador"]/text()').get().split('/')],
                projetos=projetos,
                url_perfil=pesquisador.xpath('a/@href').get(),
                image_urls=[pesquisador.xpath('.//*[@class="serra-thumb-portfolio"]/img/@src').get()]
            )
