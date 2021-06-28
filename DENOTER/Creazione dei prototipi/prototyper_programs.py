# Questo programma legge le descrizioni dei prodotti raiPlay (file descrizioni.json) 
# e scrive per ogni programma il suo prototipo 

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import treetaggerwrapper
import json
import os


#####################################################
#####################################################
#       FUNZIONI                                    #
#####################################################
#####################################################
def getLemma(word):
    tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
    return tags[0].__getattribute__("lemma").split(":")[0]


def getTypeOfWord(word):
    tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
    return tags[0].__getattribute__("pos").split(":")[0]


def isNumber(word):
    return getTypeOfWord(word) == "NUM"


def isVerb(word):
    return getTypeOfWord(word) == "VER"


def isAdjective(word):
    return getTypeOfWord(word) == "ADJ"


def isAdverb(word):
    return getTypeOfWord(word) == "ADV"


def insertProgramInDict(episode):
    program = episode["programma"]

    # Rimuovo caratteri non ammessi nella creazione di un file dal nome del programma
    for char in chars_not_allowed_in_filename:
        program = program.replace(char, "")

    description = episode["description"] + "." + episode["descrProgramma"]
    word_tokens = word_tokenize(description)
    verbo = None

    # Inserisco le parole in dict
    for word in word_tokens:
        if "'" in word:  # se la parola e' ad esempio "d'autore", prendo solo "autore"
            word = word.split("'")[1]

        word = word.lower()

        if (len(word) > 1) and (word not in remove_words) and (not isNumber(word)) and (not isAdverb(word)):

            if isVerb(word):
                verbo = getLemma(word)
            else:
                word = getLemma(word)

                # Inserisco la parola in ogni genere dell'episodio
                if program not in dict:
                    dict[program] = {}

                if word not in dict[program]:
                    dict[program][word] = 0

                dict[program][word] += 1
                if verbo is not None:
                     if verbo not in dict[program]:
                         dict[program][verbo] = 0

                     dict[program][verbo] += 1
                     verbo = None


def writeWordInFile(file, word, value):
    spaces = 20 - len(word) + 1
    stri = word + ":"
    for idx in range(spaces):
        stri = stri + " "

    stri = stri + str(value)
    file.write(stri + "\n")


#####################################################
#####################################################
#       VAR GLOBALI                                 #
#####################################################
#####################################################
language = "it"

prepositions = ["di", "a", "da", "in", "su",
                "il", "del", "al", "dal", "nel", "sul",
                "lo", "dello", "allo", "dallo", "nello", "sullo",
                "la", "della", "alla", "dalla", "nella", "sulla",
                "l’", "dell’", "all’", "dall’", "nell’", "sull’",
                "i", "dei", "ai", "dai", "nei", "sui",
                "gli", "degli", "agli", "dagli", "negli", "sugli",
                "le", "delle", "alle", "dalle", "nelle", "sulle"]
articles = ["il", "lo", "la", "i", "gli", "le", "un", "un'", "uno", "una"]
congiuntions = ["a", "a meno che", "acciocché", "adunque", "affinché", "allora",
                "allorché", "allorquando", "altrimenti", "anche", "anco", "ancorché",
                "anzi", "anziché", "appena", "avvegna che", "avvegnaché", "avvegnadioché",
                "avvengaché", "avvengadioché", "benché", "bensi", "bensì", "che", "ché",
                "ciononostante", "comunque", "conciossiaché", "conciossiacosaché", "cosicché",
                "difatti", "donde", "dove", "dunque", "e", "ebbene", "ed", "embè", "eppure",
                "essendoché", "eziando", "fin", "finché", "frattanto", "giacché", "giafossecosaché",
                "imperocché", "infatti", "infine", "intanto", "invece", "laonde", "ma", "magari",
                "malgrado", "mentre", "neanche", "neppure", "no", "nonché", "nonostante", "né", "o",
                "ogniqualvolta", "onde", "oppure", "ora", "orbene", "ossia", "ove", "ovunque",
                "ovvero", "perché", "perciò", "pero", "perocché", "pertanto", "però", "poiché",
                "poscia", "purché", "pure", "qualora", "quando", "quindi", "se", "sebbene",
                "semmai", "senza", "seppure", "sia", "siccome", "solamente", "soltanto",
                "sì", "talché", "tuttavia"]
punctuation = list(string.punctuation) + ["...", "``"]
stop_words = stopwords.words('italian')  # le stop_words sono prese dalla libreria nltk (sono parole da non considerare)
remove_words = prepositions + articles + congiuntions + punctuation + stop_words  # tutte le parole da evitare
chars_not_allowed_in_filename = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

tagger = treetaggerwrapper.TreeTagger(TAGLANG=language)

filename = "descrizioni.json"
dict = {}
path = "programs_for_cocos/"
encoding = "utf-8"
MIN_SCORE = 0.6
MAX_SCORE = 0.9

#####################################################
#####################################################
#       MAIN                                        #
#####################################################
#####################################################
if __name__ == "__main__":
    file = open(filename, "r", encoding=encoding)
    episodes = json.loads(file.read())
    file.close()

    for episode in episodes:
        insertProgramInDict(episode)

    # Controllo che la directory path esista
    if not os.path.exists(path):
        os.makedirs(path)

    # Scrivo un file per ogni programma
    for program in dict:
        # conto le parole totali del programma
        totWords = sum(dict[program].values())

        # Calcolo min e max delle medie
        minFreq = 1
        maxFreq = 0
        for word in dict[program]:
            freq = dict[program][word] / totWords
            minFreq = min(minFreq, freq)
            maxFreq = max(maxFreq, freq)


        rangeFreq = maxFreq - minFreq
        rangeScore = MAX_SCORE - MIN_SCORE

        filename = path + program + ".txt"
        file = open(filename, "w", encoding=encoding)

        # Scrivo su file le parole del programma.
        for word, count in sorted(dict[program].items(), key=lambda kv: kv[1], reverse=True):
            freq = count / totWords

            score = MAX_SCORE
            if rangeFreq > 0:
                score = MIN_SCORE + (rangeScore * (freq - minFreq) / rangeFreq)
            writeWordInFile(file, word, score)

        file.close()

    print("File generated in " + os.getcwd() + "\\" + path)
