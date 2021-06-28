import scrapy
import json

#Recupero la descrizione dell'episodio della fiction dalla pagina json
class DescrizioniEpisodi(scrapy.Spider):
    name = "descEpisodi"
    start_urls = []
    with open('./OutputFile/episodi.json') as json_file:  
        data = json.load(json_file)
        for p in data:
            for s in p["episodio"]:
                start_urls.append(str(s))

    def parse(self, response):
        jsonresponse = json.loads(response.body.decode("utf-8"))
        item = {}
        item["name"] = jsonresponse["name"]
        item["description"] = jsonresponse["description"]
        item["tipologia"] = jsonresponse["isPartOf"]["tipologia"][0]["nome"]
        item["programma"] = jsonresponse["isPartOf"]["name"]
        item["descrProgramma"] = jsonresponse["isPartOf"]["description"]
        item["generi"] = []
        #Generi
        i = 0
        for s in jsonresponse["generi"]:
            item["generi"].append(jsonresponse["generi"][i]["nome"])
            i+=1
        #Sottogeneri
        i = 0
        for s in jsonresponse["sottogeneri"]:
            item["generi"].append(jsonresponse["sottogeneri"][i]["nome"])
            i+=1

        #Problema : alcune puntate hanno genere e sottogenere dentro un altro oggetto nel json
        if(len(item["generi"]) == 0):
            #Generi
            i = 0
            for s in jsonresponse["isPartOf"]["generi"]:
                item["generi"].append(jsonresponse["isPartOf"]["generi"][i]["nome"])
                i+=1
            #Sottogeneri
            i = 0
            for s in jsonresponse["isPartOf"]["sottogenere"]:
                item["generi"].append(jsonresponse["isPartOf"]["sottogenere"][i]["nome"])
                i+=1
        return item