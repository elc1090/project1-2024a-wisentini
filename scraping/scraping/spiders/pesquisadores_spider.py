import scrapy

from scraping.items import PesquisadoresItem


class Spider(scrapy.Spider):
    name = "pesquisadores"

    custom_settings = {
        'FEEDS': {
            'data/pesquisadores.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
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
                url_imagem=pesquisador.xpath('.//*[@class="serra-thumb-portfolio"]/img/@src').get(),
                url_perfil=pesquisador.xpath('a/@href').get()
            )
