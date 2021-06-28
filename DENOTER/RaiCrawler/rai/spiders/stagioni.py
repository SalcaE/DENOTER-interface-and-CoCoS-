import scrapy
import json

#Dalla pagina specifica, in formato json, di ogni fiction, prendo link di ogni stagione
class Stagioni(scrapy.Spider):
    name = "stagioni"
    start_urls = []
    with open('./OutputFile/programmi.json') as json_file:  
        data = json.load(json_file)
        for p in data:
            start_urls.append(str(p['programma']))

    def parse(self, response):
        jsonresponse = json.loads(response.body.decode("utf-8"))
        item = {}
        i = 0
        item["name"] = jsonresponse["Name"]
        item["url"] = []
        for stagione in jsonresponse["Blocks"][0]["Sets"]:
            item["url"].append("https://www.raiplay.it" + jsonresponse["Blocks"][0]["Sets"][i]["url"])
            i+=1
        return item