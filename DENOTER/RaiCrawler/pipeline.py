import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

#Funzione che avvia spider per crawling
def run_spider(spider, file):
    def f(q):
        try:
            runner = crawler.CrawlerRunner({
                'USER_AGENT': 'Mozilla/5.0',
                'FEED_FORMAT': 'json',
                'FEED_URI': './OutputFile/' + file + '.json',
            })
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

print('Crawling per ottenere descrizioni delle fiction da Rai Play :\n')

print('1.Elenco Programmi')
from rai.spiders.programmi import Programmi
run_spider(Programmi(), 'programmi')

print('\n2.Elenco Stagioni')
from rai.spiders.stagioni import Stagioni
run_spider(Stagioni(),'stagioni')

print('\n3.Elenco Episodi')
from rai.spiders.episodi import Episodi
run_spider(Episodi(),'episodi')

print('\n4.Elenco Descrizione episodi')
from rai.spiders.descrizioniEpisodi import DescrizioniEpisodi
run_spider(DescrizioniEpisodi(),'descrizioni')

print("\nFine. Risultati nella cartella OutputFile.")
