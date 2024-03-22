import scrapy
import json

from scraping.items import PesquisadorItem


class PesquisadorSpider(scrapy.Spider):
    name = 'pesquisador'

    custom_settings = {
        'FEEDS': {
            'data/pesquisador.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        with open('data/pesquisadores.json', mode='r') as file:
            pesquisadores = json.load(file)

        urls = [pesquisador['url_perfil'] for pesquisador in pesquisadores]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_descricao(self, response):
        descricao = list()

        for paragrafo in response.xpath('//*[@class="conteudo-projeto"]//p//text()').getall():
            if not paragrafo.isspace():
                descricao.append(' '.join(paragrafo.strip().split()))

        return ' '.join(descricao)

    def parse_contatos(self, response):
        contatos = list()

        for contato in response.xpath('//*[@class="resumo-contatos"]/a'):
            eh_rede_social = bool(int(contato.xpath('starts-with(@class, "contatos-")').get()))

            if eh_rede_social:
                titulo = ' '.join(contato.xpath('@class').get().strip().split('-')[1:]).capitalize()
            else:
                titulo = contato.xpath('text()').get().strip()

            contatos.append({
                'titulo': titulo,
                'url': contato.xpath('@href').get()
            })

        return contatos

    def parse_projetos(self, response):
        projetos = list()

        for projeto in response.xpath('//*[@class="pesquisador-projeto"]'):
            projetos.append({
                'titulo': projeto.xpath('div[@class="projeto-titulo"]/text()').get().strip(),
                'areas': {area.strip() for area in projeto.xpath('following-sibling::div[1]/text()').get().split('/')},
                'texto': ''.join(projeto.xpath('following-sibling::div[1]/*[@class="projeto-texto"]//text()').getall()).strip(),
                'recursosInvestidos': [recurso.strip() for recurso in projeto.xpath('following-sibling::div[1]/*[@class="recursos"]/div//text()').getall() if not recurso.isspace()],
                'instituicoes': [instituicao.strip() for instituicao in projeto.xpath('following-sibling::div[1]//*[@class="instituicao-nome"]/text()').getall()]
            })

        return projetos

    def parse_chamadas(self, response):
        chamadas = set()

        for chamada in response.xpath('//*[@class="tags-chamadas"]/div/text()').getall():
            chamadas.add(int(chamada.strip().split()[-1]))

        return chamadas

    def parse_tags(self, response):
        tags = set()

        for tag in response.xpath('//*[@class="portfolio-tags"]//li[not(@class="chapeu")]/text()').getall():
            tags.add(tag.strip().lower())

        return tags

    def parse(self, response):
        yield PesquisadorItem(
            slug=response.url[:-1].split('/')[-1],
            descricao=self.parse_descricao(response),
            contatos=self.parse_contatos(response),
            projetos=self.parse_projetos(response),
            chamadas=self.parse_chamadas(response),
            tags=self.parse_tags(response)
        )
