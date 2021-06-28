#Crawler per Programmi (Fiction,Documentari) di RaiPlay

#HOW-TO RUN

python pipeline.py

#Output File in ./OutputFile : 

1. programmi : elenco pagine (url al file json) di ogni fiction,documentario
2. stagioni : per ogni programma, elenco pagine stagioni
3. episodi : per ogni stagione, elenco degli episodi
4. descrizioni : elenco nome, tipologia, genere, sottogenere, descrizione di ogni episodio

#File sorgenti di ogni crawler in ./rai/spiders/

#ATTENZIONE : cancellare contenuto cartella Output prima di far partire crawler, altrimenti accoda i risultati nei file
