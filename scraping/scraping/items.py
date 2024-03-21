import scrapy


class PesquisadoresItem(scrapy.Item):
    slug = scrapy.Field()
    nome = scrapy.Field()
    ano = scrapy.Field()
    areas = scrapy.Field()
    projetos = scrapy.Field()
    url_imagem = scrapy.Field()
    url_perfil = scrapy.Field()


class PesquisadorItem(scrapy.Item):
    slug = scrapy.Field()
    descricao = scrapy.Field()
    contatos = scrapy.Field()
    projetos = scrapy.Field()
    chamadas = scrapy.Field()
    tags = scrapy.Field()
