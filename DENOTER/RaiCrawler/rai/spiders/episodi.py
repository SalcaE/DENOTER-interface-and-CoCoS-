import scrapy
import json

#Dalla pagina json di ogni stagione di una fiction, prendo il link di ogni episodio
class Episodi(scrapy.Spider):
    name = "episodi"
    start_urls = []
    with open('./OutputFile/stagioni.json') as json_file:  
        data = json.load(json_file)
        for p in data:
            for s in p["url"]:
                start_urls.append(str(s))

    def parse(self, response):
        jsonresponse = json.loads(response.body.decode("utf-8"))
        item = {}
        item["episodio"] = []
        i = 0
        for s in jsonresponse["items"]:
            item["episodio"].append("https://www.raiplay.it" + jsonresponse["items"][i]["pathID"])
            i+=1
        return item