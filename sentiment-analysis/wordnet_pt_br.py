from rdflib import Graph
from rdflib.term import Literal, URIRef
import numpy as np

class WNPTBR:

    def __init__(self):
        # Loading SentiWordNet (http://sentiwordnet.isti.cnr.it/)
        self.swn = np.genfromtxt("/home/knonm/Desktop/SentiWordNet_3.0.0_20130122.txt",
            dtype=[("POS", "U1"), ("ID", "i8"), ("PosScore", "f4"), ("NegScore", "f4"), ("SynsetTerms", "U300"), ("Gloss", "U300")],
            comments=None,
            delimiter="\t",
            skip_header=27,
            skip_footer=2)

        # Loading openWordnet-PT (https://github.com/own-pt/openWordnet-PT)
        self.g = Graph()
        self.g.parse("/home/knonm/Desktop/own-pt.nt", format="nt")

    def get_synsets(self, word):
        result = []
        for i in list(self.g[::Literal(word)]):
            wordsense = i[0]
            synset = list(self.g[::wordsense])[0][0]
            synsetID = list(self.g[synset:URIRef("https://w3id.org/own-pt/wn30/schema/synsetId")])[0]
            swnEntry = self.swn[np.where(self.swn["ID"] == synsetID.toPython())[0][0]]
            result.append([swnEntry[4], synsetID, swnEntry["PosScore"], swnEntry["NegScore"]])
            # print("Word: %s | Synset: %s | PosScore: %s | NegScore: %s" % (swnEntry[4], synsetID, swnEntry["PosScore"], swnEntry["NegScore"]))
        return result
