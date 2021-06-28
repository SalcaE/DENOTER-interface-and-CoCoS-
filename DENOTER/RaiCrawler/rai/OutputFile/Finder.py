import sys
import os
import json

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

#Main : lettura generi da associare creativamente tramite argomento di linea di comando, lettura proprietà dai file, scrittura file per COCOS
if __name__ == '__main__' :
    with open('descrizioni.json') as json_file:  
        data = json.load(json_file)
        for ep in data:
            x = 0
            if contains_word(ep["description"], 'matrimonio') or contains_word(ep["name"], 'matrimonio'):
                x+=1
            if contains_word(ep["description"], 'futuro') or contains_word(ep["name"], 'futuro'):
                x+=1
            if contains_word(ep["description"], 'casa') or contains_word(ep["name"], 'casa'):
                x+=1
            if contains_word(ep["description"], 'cuore') or contains_word(ep["name"], 'cuore'):
                x+=1
            if contains_word(ep["description"], 'omicidio') or contains_word(ep["name"], 'omicidio'):
                x+=1
                   
            if x>=2 :
                print(ep["name"])
            
