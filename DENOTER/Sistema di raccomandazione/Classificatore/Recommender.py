#Classificatore che restituisce tutti gli episodi ordinati in base ad una graduatoria calcolata
#che rientrano nel nuovo genere fornito in input

import sys
import os
import json

from DataFromInput import *

#Controlla se una parola(w) e' contenuta in una stringa(s)
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def contains_value(lista, w):
    for p in lista:
        if str(p[0]) == w:
            return True
    return False

#Calcola la graduatoria e riclassifica tutti gli episodi offrendo la raccomandazione
def elaboraGraduatoria(prop_list, not_prop_list = []) :
    print("\nEpisodi raccomandati :\n\n")
        
    graduatoria = {}
    list_episodi = []
    chars_not_allowed_in_filename = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    sum = 0

    #Verifica della lista delle parole negli episodi
    with open('descr_only_lemmas.json') as json_file:  
        data = json.load(json_file)
        
        #Calcolo graduatoria
        for ep in data:
            sum = sum + 1
            for char in chars_not_allowed_in_filename:
                ep["programma"] = ep["programma"].replace(char, "")
            ep["programma"]=ep["programma"].replace("'","_")
            if ep["programma"] not in graduatoria :
                graduatoria[ep["programma"]] = 0
                for prop in prop_list:
                    if contains_word(ep["descrProgramma"], str(prop[0])) or contains_word(ep["programma"], str(prop[0])) :
                        graduatoria[ep["programma"]] = 0.1
                fileProgram = open("./programs_for_cocos/" + ep["programma"] + ".txt", "r")
                for p in fileProgram:
                    word = p.split(':')
                    if contains_value(prop_list,word[0].strip()) :
                        score = round(float(word[1].strip()),2)
                        #Inserimento episodio in graduatoria 
                        graduatoria[ep["programma"]] += score 
                fileProgram.close()               

        #Scorrimento Episodi
        for ep in data:
            for char in chars_not_allowed_in_filename:
                ep["programma"] = ep["programma"].replace(char, "")

            x = 0
            #Scorrimento proprietà risultato
            for prop in prop_list:
                if contains_word(ep["description"], str(prop[0])) or contains_word(ep["name"], str(prop[0])) or contains_word(ep["descrProgramma"], str(prop[0])) or contains_word(ep["programma"], str(prop[0])) :
                    x+=1
                    #Aumento score in caso proprietà è nel titolo o descrizione programma(come fatto in raiplay)
                    #if contains_word(ep["descrProgramma"], str(prop[0])) or contains_word(ep["programma"], str(prop[0])) :
                        #graduatoria[ep["programma"]] += 0.1
            
            #Se nell'episodio compare una proprietà negata, la puntata viene scartata
            for prop in not_prop_list:
                if contains_word(ep["description"], str(prop)) or contains_word(ep["name"], str(prop)) or contains_word(ep["descrProgramma"], str(prop)) or contains_word(ep["programma"], str(prop)) :
                    x=0
                    break
            
            #Un episodio è considerato se contiene almeno il 30% delle proprietà della lista
            if x >= int(len(prop_list)*30/100):
                list_episodi.append(ep["programma"]+ " - " + ep["name"])
            elif x == 0:
                graduatoria[ep["programma"]] = 0
    
    #Graduatoria risultato
    i = 0
    #Scorrimento graduatoria ordinata per il punteggio dei programmi in modo decrescente
    for programma, score in sorted(graduatoria.items(), key=lambda kv:kv[1], reverse=True):
        if score == 0:
            break
        i+=1
        print(programma + "-" + str(score))
        for episodio in list_episodi:
            if contains_word(episodio, programma):
                print("\n\t" + episodio)
    if i == 0 :
        print("Non ci sono contenuti raccomandabili in questa categoria.")
    else:
        perc = (100*i)/sum
        print("Classificati "+str(i)+" contenuti su "+str(sum)+" ("+str(perc)+"%)")

#Main
if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        #Lettura nome prototipo da classificare
        prototipo = sys.argv[1]

        #Lettura file prototipo - viene riutilizzato lo script "DataFromInput" di CoCoS
        f = ReadAttributes(prototipo)
        
        print("Generi  : " + f.head_conc + "_" + f.mod_conc + "\n\nClassificazione : \n")
        
        #Trasformazione risultato stringa in lista
        r = [str(s) for s in f.result.split(',')]     

        #Lista delle proprietà risultato forti + tipiche
        prop_list = []
        not_prop_list = []

        #Inserimento proprietà forti nella lista
        for p in f.attrs :
            if str(p).find('-') == -1:
                prop_list.append(p)
            else :
                not_prop_list.append(p[0].replace("-", "").strip())

        #Inserimento proprietà tipiche estratte dal risultato di COCOS
        i = 0
        for p in f.tipical_attrs:
            if r[i].strip() == "'1'":
                prop_list.append(p)
            i+=1
        pprint(prop_list)
        pprint(not_prop_list)

        #Calcolo graduatoria nuova categoria
        elaboraGraduatoria(prop_list, not_prop_list)

    elif len(sys.argv) > 2 : #Inserimento parole da linea di comando (stile ricerca rai play)
        prop_list = []
        for i in range(1,len(sys.argv)):
            prop_list.append(tuple([sys.argv[i],'1']))
        pprint(prop_list)

        #Calcolo graduatoria nuova categoria
        elaboraGraduatoria(prop_list)
    else :
        print("Inserisci il prototipo da classificare!")         
