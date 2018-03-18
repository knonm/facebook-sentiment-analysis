import sys
import csv
import treetaggerwrapper
import an
from rake_nltk import Rake
import wordnet_pt_br as wn
import tfidf

def keyword():


csv.field_size_limit(sys.maxsize)

tagger = treetaggerwrapper.TreeTagger(TAGLANG="fr")

csvfile = open("/home/knonm/Downloads/Tudo.csv", "r", newline="")
csvreader = csv.reader(csvfile, delimiter=";", quotechar="|")

rrr = Rake(language='portuguese')

tab = []
for row in csvreader:
    try:
        line = []
        line.append(an.PreprocessamentoSemStopWords(row[1].replace("¿", " "))) # Comentario
        line.append(row[6].replace("¿", " ")) # Post
        line.append(an.PreprocessamentoSemStopWords(row[10].replace("¿", " "))) # Pagina
        tab.append(line)
    except IndexError:
        None
    # tags = tagger.tag_text()
    # tags2 = treetaggerwrapper.make_tags(tags)

tab2 = tab

wnptbr = wn.WNPTBR()

tab3 = []
for r in tab2:
    try:
        line = []
        rrr.extract_keywords_from_text(r[1])
        line.append(rrr.get_ranked_phrases()[0])
        tags = tagger.tag_text(r[0])
        tags2 = treetaggerwrapper.make_tags(tags)
        pos = 0
        neg = 0
        for tg in tags2:
            aaa = wnptbr.get_synsets(tg[0])
            for bbb in aaa:
                pos += bbb[2]
                neg += bbb[3]
        if pos >= neg:
            line.append(1)
        else:
            line.append(-1)
        line.append(r[2])
        tab3.append(line)
    except:
        None
