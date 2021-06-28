import scrapy
import json

#Dalla pagina di elenco di tutte le fiction e documentari, ne prende il link della pagina principale di ognuna
#Attributo data-path
class Programmi(scrapy.Spider):
    name = "programmi"
    start_urls = [
        'https://www.raiplay.it/fiction/Tutti-bed4fa40-c8ce-41bd-9904-b8ff72c8f7ab.html',
        'https://www.raiplay.it/documentari/Tutti-19bbaa5e-eb8d-49fd-8623-7237fef7676a.html'
    ]
    def parse(self, response):
        for quote in response.css('div.small-12'):
            yield {
                'programma' : "https://www.raiplay.it" + str(quote.css('div.useraction::attr(data-path)').get()) + "?json"
            }
